import json
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    authorization_header = event['headers']['authorization']
    userId = check_authorization_header(authorization_header)
    auth = False
    if userId != "-1":
        auth = True
    
    rensponse = {
        "isAuthorized": auth,
        "context": {
            "userId": userId
        }
    }
    return rensponse;


def check_authorization_header(authorization_header):
    if not authorization_header:
        return "-1"
    
    tabellaAccounts = boto3.resource('dynamodb').Table('Accounts')
        
    response = tabellaAccounts.query(IndexName="token-index", KeyConditionExpression=Key('token').eq(authorization_header))
    
    if response['Items']:
        userId = response['Items'][0].get('id')
        return userId
    
    return "-1"
