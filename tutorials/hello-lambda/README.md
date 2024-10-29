# Hello Lambda

This is a simple project, based on the initial CDK tutorial, taken from the [offical documentation](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with a few extra features:

- The Lambda function is built with Rust on a separate project
- The code is builded and the binary is passed into the Lambda function

The Lambda function was created using Cargo Lambda, more information on how to use it for the development and test of lambda functions on [their documentation](https://www.cargo-lambda.info/guide/what-is-cargo-lambda.html).

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `npx cdk deploy`  deploy this stack to your default AWS account/region
* `npx cdk diff`    compare deployed stack with current state
* `npx cdk synth`   emits the synthesized CloudFormation template
