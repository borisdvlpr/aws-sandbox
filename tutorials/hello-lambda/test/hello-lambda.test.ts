import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { HelloLambdaStack } from '../lib/hello-lambda-stack';

describe('Given the creation of the hello-lambda stack', () => {
    describe('When the stack synthesises', () => {
        const app = new cdk.App();

        const stack = new HelloLambdaStack(app, "HelloLambdaTestStack");

        const template = Template.fromStack(stack);

        test('Then the lambda function should be created', () => {
            template.hasResourceProperties('AWS::Lambda::Function', {
                Runtime: 'provided.al2023',
                Handler: 'bootstrap',
                FunctionName: 'hello-lambda'
            });
        });

        test('Then the lambda function URL should be available', () => {          
            template.hasResourceProperties('AWS::Lambda::Url', {
                AuthType: 'NONE'
            });
        });
    });
});
