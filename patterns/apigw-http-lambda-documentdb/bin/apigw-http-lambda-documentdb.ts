#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ApigwHttpLambdaDocumentdbStack } from '../lib/apigw-http-lambda-documentdb-stack';

const app = new cdk.App();
new ApigwHttpLambdaDocumentdbStack(app, 'ApigwHttpLambdaDocumentdbStack', {
	env: { region: 'eu-central-1' }
});
