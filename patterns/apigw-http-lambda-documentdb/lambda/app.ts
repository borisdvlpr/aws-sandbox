// to further optimize the code, you can move the connection to documentdb and retrieve the secret outside the handler or through a lambda layer
// however, for simplicity, it is kept in one file

import { Handler } from "aws-cdk-lib/aws-lambda";
import { Collection, MongoClient, ObjectId } from 'mongodb';
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

export const handler: Handler = async (event: any, context: any) => {
    // add context parameter to the handler interface
    console.log('received event:', event);
    console.log('context:', context);

    // check ig the SecretString field is not undefined before trying to parse it as json
    const mongoDbUri = await getMongoDbUri();

    if(!mongoDbUri) {
        console.error('failed to retrieve MongoDB URI from secret store');

        return {
            statusCode: 500,
            body: 'internal server error - failed to retrieve MongoDB URI from the secret store.',
        };
    }

    const method = event.requestContext.http.method;
    console.log('HTTP Method:', method);

    // add a default case to the switch statement to handle unexpected HTTP methods
    const client = new MongoClient(mongoDbUri, 
        {
            tlsCAFile: `global-bundle.pem`
        },
    );

    try {
        await client.connect();

        const db = client.db('mydb');
        const collection = db.collection('mycollection');
        console.log('connected to MongoDB.')

        switch(method) {
            case 'GET':
                return await handleGetRequest(collection);
            case 'POST':
                return await handlePostRequest(event, collection);
            case 'PUT':
                return await handlePutRequest(event, collection);
            case 'DELETE':
                return await handleDeleteRequest(event, collection);
            default:
                return handleUnsupportedMethod();
        }

    } finally {
        await client.close();
        console.log('MongoDB client closed.')
    }
};

async function handleGetRequest(collection: Collection) {
    const data = await collection.find({}).toArray();
    console.log('fetched data:', data);
    
    return {
        statusCode: 200,
        body: JSON.stringify(data),
    };
}

async function handlePostRequest(event: any, collection: Collection) {
    const payload = event.body ? JSON.parse(event.body) : {};
    console.log('received payload:', payload);
    const result = await collection.insertOne(payload);
    console.log('inserted data:', result)
    
    return {
        statusCode: 201,
        body: JSON.stringify(result),
    }
}

async function handlePutRequest(event: any, collection: Collection) {
    const updatedPayload = event.body ? JSON.parse(event.body) : {};
    console.log('updated payload:', updatedPayload);

    const filter = { _id: new ObjectId(updatedPayload._id) };
    delete updatedPayload._id;

    const result = await collection.updateOne(filter, { $set: updatedPayload });
    console.log('updated data:', result);
    
    return {
        statusCode: 200,
        body: JSON.stringify(result),
    }
}

async function handleDeleteRequest(event: any, collection: Collection) {
    const idToDelete = event.queryStringParameters._id;

    try {
        const filter = { _id: new ObjectId(idToDelete) };

        const result = await collection.deleteOne(filter)
        console.log('deleted data:', result);

        return {
            statusCode: 200,
            body: JSON.stringify(result),
        }

    } catch(error) {
        console.error('error deleting document:', error);

        return {
            statusCode: 500,
            body: 'internal server error - failed to delete document.',
        }
    }
}

function handleUnsupportedMethod() {
    console.log('unsupported HTTP method.');

    return {
        statusCode: 400,
        body: 'unsupported HTTP method.'
    }
}

// get MongoDB URI from secrets manager
async function getMongoDbUri() {
    try {
        const secret_name = process.env.DOCUMENT_SECRET_NAME;
        const client = new SecretsManagerClient();
        const response = await client.send(
            new GetSecretValueCommand({
                SecretId: secret_name,
                VersionStage: 'AWSCURRENT',
            })
        );

        if(typeof response.SecretString !== 'undefined') {
            const { host, password, username, port } = JSON.parse(response.SecretString);
            const DOCDB_ENDPOINT = host || 'DOCDBURL';
            const DOCDB_PASSWORD = encodeURIComponent(password) || 'DOCPASSWORD';
            const DOCDB_USERNAME = username || 'myuser';
            const DOCDB_PORT = port || 'port';

            const uri = `mongodb://${DOCDB_USERNAME}:${DOCDB_PASSWORD}@${DOCDB_ENDPOINT}:${DOCDB_PORT}/mydb?tls=true&replicaSet=rs0&        readPreference=secondaryPreferred&retryWrites=false`;

            return uri;
        }

    } catch(error) {
        console.error('Error retrieving MongoDB URI:', error);
    }

    return null;
}
