import aws_cdk as cdk
from aws_cdk import (
    aws_apigateway as _apigw,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_s3 as s3,
    RemovalPolicy,
    Stack
)
from constructs import Construct
import os


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

        # s3 bucket for weekly data summaries
        summary_bucket = s3.Bucket(
            self, 
            "CarDataSummaryBucket",
            bucket_name = f"car-data-summaries-{self.account}-{self.region}",
            versioned = True,
            encryption = s3.BucketEncryption.S3_MANAGED,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True
        )

        # rest api lambda function
        api_lambda = _lambda.Function(
            self, 
            "api_lambda",
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda/api-handler.zip")),
            handler = "index.handler",
            environment = {
                "TABLE_NAME": car_table.table_name,
            }
        )

        # weekly summary lambda function
        summary_lambda = _lambda.Function(
            self,
            "summary_lambda",
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda/summary-handler.zip")),
            handler = "index.handler",
            environment = {
                "BUCKET_NAME": summary_bucket.bucket_name,
                "TABLE_NAME": car_table.table_name,
            }
        )

        # grant permissions
        car_table.grant_write_data(api_lambda)
        car_table.grant_read_data(summary_lambda)
        summary_bucket.grant_write(summary_lambda)

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

        # request model for validation
        car_model = apigw.add_model(
            "CarModel",
            content_type = "application/json",
            schema = _apigw.JsonSchema(
                type = _apigw.JsonSchemaType.OBJECT,
                properties = {
                    "brand": _apigw.JsonSchema(
                        type = _apigw.JsonSchemaType.STRING,
                        min_length = 1,
                        max_length = 50
                    ),
                    "model": _apigw.JsonSchema(
                        type = _apigw.JsonSchemaType.STRING,
                        min_length = 1,
                        max_length = 100
                    ),
                    "year": _apigw.JsonSchema(
                        type = _apigw.JsonSchemaType.INTEGER,
                        minimum = 1900,
                        maximum = 2030
                    ),
                    "engine_cc": _apigw.JsonSchema(
                        type = _apigw.JsonSchemaType.INTEGER,
                        minimum = 1000,
                        maximum = 8000
                    )
                },
                required = ["brand", "model", "year", "engine_cc"]
            )
        )

        car_validator = apigw.add_request_validator(
            "CarDataValidator",
            validate_request_body = True,
        )
        
        # api resources and methods
        cars_resource = apigw.root.add_resource("cars")
        cars_resource.add_method(
            "POST",
            request_validator = car_validator,
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
