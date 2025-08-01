import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_apigateway as _apigw,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    RemovalPolicy,
    Stack
)
from constructs import Construct

class ScheduledDataSummaryExportStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # dynamodb table for car data
        car_table = dynamodb.Table(
            self, 
            "CarDataTable",
            table_name = "car-data",
            partition_key = dynamodb.Attribute(
                name = "id",
                type = dynamodb.AttributeType.STRING
            ),
            billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST,
            encryption = dynamodb.TableEncryption.AWS_MANAGED,
            removal_policy = RemovalPolicy.DESTROY
        )

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

        # api gateway
        apigw = _apigw.LambdaRestApi(
            self, 
            "car_data_apigw",
            rest_api_name="Car Data Service",
            description="API for car data collection",
            handler=api_lambda,
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_origins=_apigw.Cors.ALL_ORIGINS,
                allow_methods=["POST"],
                allow_headers=["Content-Type"]
            ),
        )
        
        # api resources and methods
        cars_resource = apigw.root.add_resource("cars")
        cars_resource.add_method(
            "POST",
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_models={"application/json": _apigw.Model.EMPTY_MODEL}
                ),
                _apigw.MethodResponse(
                    status_code="400",
                    response_models={"application/json": _apigw.Model.ERROR_MODEL}
                ),
                _apigw.MethodResponse(
                    status_code="500",
                    response_models={"application/json": _apigw.Model.ERROR_MODEL}
                )
            ]
        )

        # api gateway url output
        cdk.CfnOutput(
            self, "ApiGatewayUrl",
            value=apigw.url,
            description="API Gateway endpoint URL"
        )
