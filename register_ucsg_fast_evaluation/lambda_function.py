import json
import boto3

def lambda_handler(event, context):
    
    # Reading 'body' from event
    body = event.get("body")
    body_json = json.loads(body)

    if not body_json:
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid payload")
        }

    # Return error mesage if the user payload does not have enough info
    if not body_json.get("identification"):
        return {
            "statusCode": 400,
            "body": json.dumps("No identification found in payload")
        }
    
    if not body_json.get("password"):
        return {
            "statusCode": 400,
            "body": json.dumps("No password found in payload")
        }

    # user_payload = json.loads(body)
    user_payload = {}
    user_payload["id"] = body_json.get("identification")
    user_payload["password"] = body_json.get("password")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CommunityUsers')
    response = table.put_item(
        Item = user_payload
    )

    # Response for the client
    data = {
        "message": "User was created",
        "user": user_payload
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
    }
