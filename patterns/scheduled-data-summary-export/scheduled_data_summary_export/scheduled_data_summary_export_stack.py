import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_apigateway as _apigw,
    aws_lambda as _lambda,
)
from constructs import Construct

class ScheduledDataSummaryExportStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # rest api lambda function
        api_lambda = _lambda.Function(
            self, 
            "api_lambda",
            runtime = _lambda.Runtime.NODEJS_22_X,
            handler = "index.handler",
            code = _lambda.Code.from_inline(
                """
                exports.handler = async function(event) {
                    return {
                        statusCode: 200,
                        body: JSON.stringify('Hello World!'),
                    };
                };
                """
            ),
        )
