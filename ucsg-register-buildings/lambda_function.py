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

    # Return error mesage if the user payload does not have enough info
    if not building_payload.get("userId"):
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid userId in payload")
        }

    if not building_payload.get("userName"):
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid userName in payload")
        }

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Buildings')

    # This was commented to be able to register more than one building of the user
    """""
    building_exists = check_user_buildings(building_payload["userId"], table)

    # Create an id if the element doesn't exists
    if not building_exists:
        building_payload["id"] = str(uuid.uuid4())
    else:
        building_payload["id"] = building_exists[0]["id"]
    """""
    building_payload["id"] = str(uuid.uuid4())

    # Creating user in database
    response = table.put_item(
        Item=building_payload
    )

    # Response for the client
    data = {
        "message": "Building was created",
        "user": building_payload
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        }
    }


def check_user_buildings(user_id, table):

    # Searching buildings of the user in the dynamodb
    response = table.query(
        IndexName="userId-index",
        KeyConditionExpression="userId = :usr",
        ExpressionAttributeValues={
            ":usr": user_id,
        },

    )

    buildings = response.get('Items', {})

    return buildings
