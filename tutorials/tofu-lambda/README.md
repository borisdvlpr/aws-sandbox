# Tofu Lambda

This is a simple project, based on the initial CDK tutorial, taken from the [offical documentation](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with a few extra features:

- The infrastructure is defined using OpenTofu
- The lambda function is built with Rust on a separate project
- The infrastructure is applied and the binary is passed into the lambda function

The lambda function was created using Cargo Lambda, more information on how to use it for the development and test of lambda functions on [their documentation](https://www.cargo-lambda.info/guide/what-is-cargo-lambda.html).
