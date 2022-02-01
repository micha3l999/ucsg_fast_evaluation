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

    if not body_json.get("building_id"):
        return {
            "statusCode": 400,
            "body": json.dumps("No building id in payload")
        }

    # get user data from database
    building_id = body_json.get("building_id")

    print(building_id)

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Buildings")
    response = table.query(
        KeyConditionExpression=Key('id').eq(building_id)
    )
    print(response)
    building = response.get('Items', [])[0]

    # Check if user exists
    if not building:
        return {
            "statusCode": 409,
            "body": json.dumps("The user doesn't have any buildings")
        }
    
    data = {
        "message": "success",
        "building": building
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }