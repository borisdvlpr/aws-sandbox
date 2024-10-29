import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class HelloLambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define the Lambda function resource
    const helloFunction = new lambda.Function(this, "HelloLambdaFunction", {
        code: lambda.Code.fromAsset(path.join(__dirname, "lambdas/hello-lambda/target/lambda/hello-lambda")),
        runtime: lambda.Runtime.PROVIDED_AL2023,
        handler: "bootstrap",
        functionName: "hello-lambda"
    });

    // Define the Lambda function URL resource
    const myFunctionUrl = helloFunction.addFunctionUrl({
        authType: lambda.FunctionUrlAuthType.NONE,
    });

    // Define a CloudFormation output for your URL
    new cdk.CfnOutput(this, "myFunctionUrlOutput", {
        value: myFunctionUrl.url,
    })
  }
}
