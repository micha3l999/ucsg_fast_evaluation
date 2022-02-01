import json
import boto3

def lambda_handler(event, context):
    
    #  Reading events
    body = event.get("body")

    if not body:
        return {
            "statusCode": 400,
            "body": json.dumps("No query parameters found")
        }
    # Return an error message if the data was not founded
    body_json = json.loads(body)

    if not body_json.get("building_id"):
        return {
            "statusCode": 400,
            "body": json.dumps("No building id in payload")
        }
    
    if not body_json.get("user_id"):
        return {
            "statusCode": 400,
            "body": json.dumps("No user id in payload")
        }

    # get user data from database
    building_id = body_json.get("building_id")
    user_id = body_json.get("user_id")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Buildings")
    response = table.delete_item(
        Key = {
            'id': building_id,
            'userId': user_id,
        },
    )
    
    data = {
        "message": "success",
        "building": "Building deleted"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }