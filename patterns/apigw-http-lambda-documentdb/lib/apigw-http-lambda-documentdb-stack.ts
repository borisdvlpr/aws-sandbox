import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import * as docdb from 'aws-cdk-lib/aws-docdb';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { Construct } from 'constructs';

export class ApigwHttpLambdaDocumentdbStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		const documentDBSecretName = 'documentDbSecretName';

		// create vpc with public and private subnets
		const vpc = new ec2.Vpc(this, 'VPC-serverless-pattern', {
			ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
			maxAzs: 2, 
			subnetConfiguration: [
				{ cidrMask: 24, name: 'PublicSubnet', subnetType: ec2.SubnetType.PUBLIC },
				{ cidrMask: 24, name: 'PrivateSubnet', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
			],
			natGateways: 1
		});

		// create api gateway
		const httpApi = new apigw.HttpApi(this, 'HttpApiGateway', {
			apiName: 'ApiGatewayToLambda',
			description: 'Integration between API Gateway HTTP and Lambda function',
		});

		// create documentdb in the private subnet of the vpc
		const docDbCluster = new docdb.DatabaseCluster(this, 'Database', {
			masterUser: {
				username: 'myuser',					//NOTE: 'admin' is reserved by documentdb
				excludeCharacters: "\"@/:",			//OPTIONAL: defaults to the set "\"@/" and is also used for eventually created rotations
				secretName: documentDBSecretName,	//OPTIONAL: if you prefer to specify the secret name
			},
			instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
			vpcSubnets: {
				subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
			},
			vpc: vpc
		});

		// allow documentdb access from the vpc
		docDbCluster.connections.allowFrom(ec2.Peer.ipv4(vpc.vpcCidrBlock), ec2.Port.tcp(27017));

		// destroy documentdb cluster when stack is destroyed - remove the production use
		docDbCluster.applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);

		// aws secrets manager secret for the documentdb
		const dbSecret = docDbCluster.secret!

		// lambda function which is connected to the documentdb
		const lambdaToDocumentDb = new NodejsFunction(this, 'LambdaToDocumentDB', {
			runtime: Runtime.NODEJS_20_X,
			handler: 'main.handler',
			timeout: cdk.Duration.seconds(300),
			entry: path.join(__dirname, '../lambda/app.ts'),
			environment: {
				DOCUMENTDB_SECRET_NAME: documentDBSecretName,
			},
			vpc: vpc,	// lambda needs to be in the vpc which has a route to the documentdb database
			vpcSubnets: {
				subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
			},
			bundling: {
				commandHooks: {
					afterBundling: (inputDir: string, outputDir: string): string[] => [
						`cp ${inputDir}/lambda/global-bundle.pem ${outputDir}`
					],
					beforeBundling: (inputDir: string, outputDir: string): string[] => [],
					beforeInstall: (inputDir: string, outputDir: string): string[] => [],
				},
			},
		});

		// grant lambda access to aws secrets manager secret
		lambdaToDocumentDb.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
			actions: ['secretsmanager:GetSecretValue'],
			resources: [dbSecret.secretFullArn!],
			effect: cdk.aws_iam.Effect.ALLOW
		}));
	}
}
