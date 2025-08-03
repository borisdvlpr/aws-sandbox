import boto3
import datetime
import json
import logging
import os
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any
import uuid


# configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# initialize dynamodb client
dynamodb = boto3.resource('dynamodb')

class CarData(BaseModel):
    brand: str = Field(..., min_length=1, max_length=50, description="Car brand")
    model: str = Field(..., min_length=1, max_length=100, description="Car model name")
    year: int = Field(..., ge=1900, le=2030, description="Manufacturing year")
    engine_cc: int = Field(..., ge=1000, le=8000, description="Engine displacement in CC")

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for car data API endpoint
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    # get http method and resource
    http_method = event.get('httpMethod')
    resource = event.get('resource', '')

    # get table name from environment
    table_name = os.environ.get('TABLE_NAME')
    if not table_name:
        logger.error("TABLE_NAME environment variable not set")
        return create_error_response(500, 'Configuration error', 'Database configuration missing')
    
    if http_method == "POST" and resource == "/cars":
        return create_car(table_name, event)
    else:
        return create_error_response(405, 'Method Not Allowed', f'Method {http_method} not supported')
    
def create_car(table_name: str, event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new car item to DynamoDB.

    Args:
        table_name: Name of the DynamoDB table.
        event: API Gateway event containing the request body.

    Returns:
        API Gateway response indicating success or error.
    """
    # validate request body existance
    if 'body' not in event or not event['body']:
        logger.error("Request error: missing request body")
        return create_error_response(400, 'Missing request body', 'Request body is required')
    
    # parse JSON body
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return create_error_response(400, 'Invalid JSON', 'Request body must be valid JSON')
    
    # validate car data
    try:
        car_data = CarData(**body)
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_error_response(400, 'Validation failed', 'Invalid car data format', e.errors())

    # create new dynamodb item
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z'
    new_car = {
        'id': str(uuid.uuid4()),
        'timestamp': current_time,
        'brand': car_data.brand,
        'model': car_data.model,
        'year': car_data.year,
        'engine_cc': car_data.engine_cc,
        'created_at': current_time,
        'updated_at': current_time
    }
    
    # save new item to dynamodb
    try:
        dynamodb.Table(table_name).put_item(Item=new_car)
        logger.info(f"Successfully stored car data with ID: {new_car['id']}")
    except Exception as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return create_error_response(500, 'Database error', 'Failed to store car data')
    
    # return success response
    return create_response(200, {
        'message': 'Car data stored successfully',
        'id': new_car['id'],
        'timestamp': new_car['timestamp']
    })

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
