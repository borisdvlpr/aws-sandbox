# Tofu Lambda

This project demonstrates how to deploy an AWS Lambda function written in Rust using [Cargo Lambda](https://www.cargo-lambda.info/guide/what-is-cargo-lambda.html) and provisioned with [OpenTofu](https://opentofu.org/). It is inspired by the [official AWS CDK hello world tutorial](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with a few enhancements.

## Features

- **Infrastructure as Code:** Define and manage AWS resources using OpenTofu
- **Rust Lambda:** Build and package the Lambda function in Rust using Cargo Lambda
- **State Management:** Automatically create and configure resources for OpenTofu state management (e.g., S3 bucket, DynamoDB table).

## Project Structure

- `infra/` – OpenTofu configuration files for AWS resources and state management.
- `lambdas/hello-lambda` – Rust source code for the Lambda function.

## Usage

1. **Build the Lambda Function:**

```sh
cd lambda/hello-lambda
cargo lambda build --release
```

2. **Deploy Infrastructure:**

```sh
cd infra
tofu init
tofu plan
tofu apply
```

3. **Invoke the Lambda**: Call the Lambda function using the URL provided in the OpenTofu output or thorugh the AWS Console.
