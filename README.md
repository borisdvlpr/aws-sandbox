# aws-sandbox

[![Built with Devbox](https://www.jetify.com/img/devbox/shield_moon.svg)](https://www.jetify.com/devbox/docs/contributor-quickstart/)

![AWS Logo](./assets/aws_logo.png)

## Intro

This repo contains a collection of examples, patterns and other AWS projects built with CDK and OpenTofu. 

## Getting started

To get started, the following dependencies need to be installed:

- [Devbox](https://www.jetify.com/docs/devbox/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting-started.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

If you'd rather not use Devbox, you can manually install the dependencies listed in the `devbox.json` file under the "packages" section.

## Resources

In this repo, the following resources are available:

#### **Tutorials**

- [hello-lambda](tutorials/hello-lambda/) - first AWS CDK app, taken from the [offical documentation](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with some salt (and Rust)
- [tofu-lambda](tutorials/tofu-lambda/) - implementation of the first CDK app in OpenTofu (and Rust)

#### **Patterns**

- [apigw-http-lambda-documentdb](patterns/apigw-http-lambda-documentdb/) - API Gateway integration with Lambda and DocumentDB

## Contributing

Feel free to open any issues on pull requests!
