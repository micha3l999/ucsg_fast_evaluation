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

    user_payload = {}
    user_payload["id"] = body_json.get("identification")
    user_payload["name"] = body_json.get("name")
    user_payload["address"] = body_json.get("address")
    user_payload["age"] = body_json.get("age")
    user_payload["password"] = body_json.get("password")

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CommunityUsers')

    user_exists = check_user_created(user_payload["id"], table)

    if not user_exists:
        return {
            "statusCode": 400,
            "body": json.dumps("User doesn't exists")
        }

    # Creating user in database
    response = table.update_item(
        Key =  {
            'id': user_payload["id"],
        },
        UpdateExpression = "set #nm=:n, age=:a, address=:ad, password=:pss",
        ExpressionAttributeValues= {
            ':n': user_exists["name"] if not user_payload["name"] else user_payload["name"],
            ':a': user_exists["age"] if not user_payload["age"] else user_payload["age"],
            ':ad': user_exists["address"] if not user_payload["address"] else user_payload["address"],
            ':pss': user_exists["password"] if not user_payload["password"] else user_payload["password"],
        },
        ExpressionAttributeNames = {
            "#nm": "name"
        },
        ReturnValues = "UPDATED_NEW"
    )

    # Response for the client
    data = {
        "message": "User was updated",
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

def check_user_created(identification, table):

    # Searching user in database
    response = table.get_item(
        Key = {
            'id': identification
        }
    )

    user = response.get('Item', {})
    
    return user