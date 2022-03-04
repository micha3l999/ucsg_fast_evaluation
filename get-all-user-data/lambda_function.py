import json
import boto3


def lambda_handler(event, context):

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Buildings')

    # Retrieving all information about buildings
    scan_args = {
        'ProjectionExpression': "id, userName, userId, cadastralCode"
    }

    done = False
    start_key = None
    items = None
    while not done:
        if start_key:
            scan_args['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_args)
        items = response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    # Response for the client
    data = {
        "message": "All data retrieved",
        "buildings": items
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        }
    }
