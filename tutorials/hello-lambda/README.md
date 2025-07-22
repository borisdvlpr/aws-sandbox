# Hello Lambda

This project demonstrates how to deploy an AWS Lambda function written in Rust using [Cargo Lambda](https://www.cargo-lambda.info/guide/what-is-cargo-lambda.html) and provision it with AWS CDK. It is based on the [official AWS CDK hello world tutorial](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with a few enhancements.

## Features

- **Rust Lambda:** Build and package the Lambda function in Rust using Cargo Lambda
- **Automated Deployment:** The Lambda binary is built and passed to the function automatically during deployment.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Project Structure

- `infra/` – AWS CDK configuration files for AWS resources.
- `lambdas/hello-lambda` – Rust source code for the Lambda function.

## Usage

1. **Build the Lambda Function:**

```sh
cd lambdas/hello-lambda
cargo lambda build --release
```

2. **Deploy Infrastructure:**

```sh
cdk bootstrap
cdk synth
cdk deploy
```

For more detailed information on how to deploy the CDK code please refer to the [official AWS CDK hello world tutorial](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html).

3. **Invoke the Lambda:** Call the Lambda function using the AWS Console or AWS CLI.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `npx cdk deploy`  deploy this stack to your default AWS account/region
* `npx cdk diff`    compare deployed stack with current state
* `npx cdk synth`   emits the synthesized CloudFormation template
