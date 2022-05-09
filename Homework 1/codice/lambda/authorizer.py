import json
import base64
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    #print(event)
    
    authorization_header = event['headers']['authorization']
    auth = check_authorization_header(authorization_header)

    
    rensponse = {
        "isAuthorized": auth,
        "context": {
            "anyotherparam": "values"
        }
    }
    return rensponse;


def check_authorization_header(authorization_header):
    if not authorization_header:
        return False
    
    tabellaAccounts = boto3.resource('dynamodb').Table('Accounts')
    response = tabellaAccounts.query(KeyConditionExpression=Key('token').eq(authorization_header))
    
    if response['Items']:
        return True
    
    return False
