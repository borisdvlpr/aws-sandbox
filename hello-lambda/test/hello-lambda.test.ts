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
                Runtime: 'python3.12',
                Handler: 'index.handler',
                Code: {
                    ZipFile: `
          def handler(event, context):
              return {
                  'statusCode': 200,
                  'body': 'hello, world'
              }
        `
                }
            });
        });
    });
});
