import json
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler

    :param event: dict, the event data sent by the requester
    :param context: LambdaContext, runtime information
    :return: dict,
    """

    body = {"message": "Hello Lambda!"}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }