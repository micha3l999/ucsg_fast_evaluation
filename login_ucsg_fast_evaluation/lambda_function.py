import json
import boto3

def lambda_handler(event, context):
    #  Reading events
    body = event.get("body")

    if not body:
        return {
            "statusCode": 400,
            "body": json.dumps("No data founded in body")
        }

    # Return an error message if the data was not founded
    body_json = json.loads(body)

    if not body_json.get("identification"):
        return {
            "statusCode": 400,
            "body": json.dumps("No identification founded in payload")
        }

    if not body_json.get("password"):
        return {
            "statusCode": 400,
            "body": json.dumps("No password founded in payload")
        }

    # Check user in database
    user_identification = body_json.get("identification")
    user_password = body_json.get("password")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("CommunityUsers")
    response = table.get_item(
        Key = {
            'id': user_identification
        }
    )
    user = response.get('Item', {})

    # Check database with request password
    if user.get("password") != user_password:
        return {
            "statusCode": 401,
            "body": json.dumps("The password is incorrect")
        }
    
    data = {
        "message": "Login succesfully",
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