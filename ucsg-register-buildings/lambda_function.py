import json
import boto3
import uuid

def lambda_handler(event, context):
    
    # Reading 'body' from event
    body = event.get("body")

    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Not valid payload")
        }

    building_payload = json.loads(body)
    building_payload["id"] = str(uuid.uuid4())

    # Return error mesage if the user payload does not have enough info
    if not building_payload.get("userId"):
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid userId in payload")
        }
    
    if not building_payload.get("inspectorIdentification"):
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid inspectorIdentification in payload")
        }
    
    if not building_payload.get("structureType"):
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid structureType in payload")
        }    

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Buildings')

    # Search if the user's building is already registered


    # Check user in the database
    """
    building_exists = check_user_building(building_payload["userId"], table)
    
    if building_exists:
        return {
            "statusCode": 409,
            "body": json.dumps("Building exists")
        }
    """

    # Creating user in database
    response = table.put_item(
        Item = {
            "userId": building_payload.get("userId"),
        },
        ConditionExpression = {
            'attribute_not_exists(userId)'
        }
    )

    # Response for the client
    data = {
        "message": "Building was created",
        "user": response
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
    }

def check_user_building(user_id, table):

    # Searching user in database
    response = table.get_item(
        ExpressionAttributeValues = {

        },
        FilterExpression = {

        },
    )

    user = response.get('Item', {})

    if not user:
        return False
    
    return True

