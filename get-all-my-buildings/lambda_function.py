import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    #  Reading events
    path_parameters = event.get("pathParameters")

    if not path_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps("No path parameters found")
        }

    # Return an error message if the data was not founded
    body_json = path_parameters

    if not body_json.get("userId"):
        return {
            "statusCode": 400,
            "body": json.dumps("No user id in payload")
        }
    userId = body_json.get("userId")

    # get user data from database
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Buildings")
    response = table.query(
        IndexName="userId-index",
        KeyConditionExpression=Key('userId').eq(userId),
        ProjectionExpression="id, userName, userId",
    )

    buildings = response.get('Items', [])

    data = {
        "message": "success",
        "buildings": buildings
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
