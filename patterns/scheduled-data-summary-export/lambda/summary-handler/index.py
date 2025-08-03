import json
import boto3
import logging
import os
import datetime
from typing import Dict, Any


# configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# initialize dynamodb and s3 clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler to generate a simple summary of car data and upload to S3.

    - Counts total items in the DynamoDB table.
    - Lists all items, one per line in the summary file.
    """

    try:
        # get table and bucket names from environment
        table_name = os.environ.get('TABLE_NAME')
        bucket_name = os.environ.get('BUCKET_NAME')
        if not table_name or not bucket_name:
            return create_error_response(500, 'Configuration error', 'Bucket or database configuration missing')
        
        items = []

        # read all items from dynamodb
        try:
            table = dynamodb.Table(table_name)
            response = table.scan()
            items.extend(response.get('Items', []))
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))
        except Exception as e:
            logger.error(f"DynamoDB error: {str(e)}")
            return create_error_response(500, 'Database error', 'Failed to store car data')

        # prepare summary content
        summary_lines = [
            json.dumps({"total_count": len(items)}),
            *(json.dumps(item, default = str) for item in items)
        ]
        summary_content = "\n".join(summary_lines)

        # upload to s3 bucket
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z'
        s3_key = f"car-data-summary-{timestamp}.json"
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=summary_content.encode('utf-8'),
            ContentType='application/json'
        )

        logger.info(f"Successfully uploaded summary to S3: {s3_key}")
        return create_response(200, {
                "message": "Summary generated and uploaded",
                "s3_key": s3_key,
                "total_count": len(items)
            })

    except Exception as e:
        logger.error(f"Error in weekly summary generation: {str(e)}")
        return create_error_response(500, "Summary generation failed", str(e))
    
def create_response(status_code: int, body: Any) -> Dict[str, Any]:
    """
    Create a standardized API response.

    Args:
        status_code: HTTP status code for the response.
        body: Response body to be serialized as JSON.

    Returns:
        Dictionary formatted as an API Gateway response.
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST'
        },
        'body': json.dumps(body)
    }

def create_error_response(status_code: int, error: str, message: str, details: Any = None) -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        status_code: HTTP status code for the error response.
        error: Short error type or code.
        message: Human-readable error message.
        details: Additional error details (optional).

    Returns:
        Dictionary formatted as an API Gateway error response.
    """
    body = {'error': error, 'message': message}
    if details:
        body['details'] = details
    return create_response(status_code, body)
