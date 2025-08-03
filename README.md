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

All additional dependencies required for each tutorial and pattern are managed and available through Devbox. If you'd rather not use Devbox, you can manually install the dependencies found in each project, also defined in the `devbox.json` file under the "packages" section.

## Resources

In this repo, the following resources are available:

#### **Tutorials**

- [hello-lambda](tutorials/hello-lambda/) - first AWS CDK app based on the [offical documentation](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html), with enhancements and a Rust implementation
- [tofu-lambda](tutorials/tofu-lambda/) - example of building the first CDK app using OpenTofu and Rust

#### **Patterns**

- [apigw-http-lambda-documentdb](patterns/apigw-http-lambda-documentdb/) - pattern demonstrating how to expose a REST API with API Gateway, process requests using Lambda, and persist data in DocumentDB
- [scheduled-data-summary-export](patterns/scheduled-data-summary-export/) - pattern for ingesting JSON data via an API endpoint, persisting it to a datastore, and generating weekly summary files with item counts, stored in S3

## Contributing

Feel free to open any issues on pull requests!
