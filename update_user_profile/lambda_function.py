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
    if not body_json.get("name"):
        return {
            "statusCode": 400,
            "body": json.dumps("No name found in payload")
        }

    if not body_json.get("age"):
        return {
            "statusCode": 400,
            "body": json.dumps("No age found in payload")
        }

    if not body_json.get("address"):
        return {
            "statusCode": 400,
            "body": json.dumps("No address found in payload")
        }
    
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

    user_payload = {}
    user_payload["id"] = body_json.get("identification")
    user_payload["password"] = body_json.get("password")
    user_payload["name"] = body_json.get("name")
    user_payload["address"] = body_json.get("address")
    user_payload["age"] = body_json.get("age")

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CommunityUsers')

    # Creating user in database
    response = table.update_item(
        Key =  {
            'id': user_payload["id"],
        },
        UpdateExpression = "set id=:i, name=:n, age=:a, address=:ad, password=:p",
        ExpressionAttributesValues= {
            ':i': user_payload["id"],
            ':n': user_payload["name"],
            ':a': user_payload["age"],
            ':ad': user_payload["address"],
            ':p': user_payload["password"],
        },
        ReturnValues = "UPDATED_NEW"
    )

    user_updated = response.get('Item', {})

    # Response for the client
    data = {
        "message": "User was updated",
        "user": user_updated
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
    }