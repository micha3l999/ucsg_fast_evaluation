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
    if not body_json.get("buildingId"):
        return {
            "statusCode": 400,
            "body": json.dumps("No building id found in payload")
        }

    if not body_json.get("userId"):
        return {
            "statusCode": 400,
            "body": json.dumps("No userId found in payload")
        }

    if not body_json.get("inspectorIdentification"):
        return {
            "statusCode": 400,
            "body": json.dumps("No inspector identification found in payload")
        }

    # Getting dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Buildings')

    # Updating buildings database
    response = table.update_item(
        Key =  {
            'id': body_json["buildingId"],
            'userId': body_json["userId"],
        },
        UpdateExpression = "set buildingQualification=:bql, inspectionPlace=:inpl, installationAddress=:adss, restrictions=:rtss, inspectorObservation=:iob, emergencyComments=:ecm, inspectorIdentification=:iidt",
        ExpressionAttributeValues= {
            ':bql': body_json.get("buildingQualification"),
            ':inpl': body_json.get("inspectionPlace"),
            ':adss': body_json.get("installationAddress"),
            ':rtss': body_json.get("restrictions"),
            ':iob': body_json.get("inspectorObservation"),
            ':ecm': body_json.get("emergencyComments"),
            ':iidt': body_json.get("inspectorIdentification"),
        },
        ReturnValues = "UPDATED_NEW"
    )

    # Response for the client
    data = {
        "message": "User was updated",
        "user": body_json
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
    }