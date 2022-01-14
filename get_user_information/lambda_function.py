import json
import boto3

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

    if not body_json.get("user_identification"):
        return {
            "statusCode": 400,
            "body": json.dumps("No identification founded in payload")
        }

    # get user data from database
    user_identification = body_json.get("user_identification")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("CommunityUsers")
    response = table.get_item(
        Key = {
            'id': user_identification
        }
    )
    user = response.get('Item', {})

    # Check if user exists
    if not user:
        return {
            "statusCode": 409,
            "body": json.dumps("The user is not registered")
        }

    del user["password"]
    
    data = {
        "message": "success",
        "user": user
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }