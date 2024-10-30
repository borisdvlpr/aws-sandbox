import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as apigw from 'aws-cdk-lib/aws-apigatewayv2';
import * as docdb from 'aws-cdk-lib/aws-docdb';
import { Construct } from 'constructs';

export class ApigwHttpLambdaDocumentdbStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		const documentDBSecretName = 'documentDbSecretName';

		//create vpc with public and private subnets
		const vpc = new ec2.Vpc(this, 'VPC-serverless-pattern', {
			ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),
			maxAzs: 2, 
			subnetConfiguration: [
				{ cidrMask: 24, name: 'PublicSubnet', subnetType: ec2.SubnetType.PUBLIC },
				{ cidrMask: 24, name: 'PrivateSubnet', subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
			],
			natGateways: 1
		});

		//create api gateway
		const httpApi = new apigw.HttpApi(this, 'HttpApiGateway', {
			apiName: 'ApiGatewayToLambda',
			description: 'Integration between API Gateway HTTP and Lambda function',
		});

		//create documentdb in the private subnet of the vpc
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
	}
}
