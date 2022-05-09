import json
import boto3
from boto3.dynamodb.conditions import Key
import base64

def lambda_handler(event, context):
    try:
        bucketName = 'xmlresults'
        s3 = boto3.resource('s3')
        tabellaListaGare = boto3.resource('dynamodb').Table('ListaGare')
        s3Client = boto3.client('s3')
        idDaCercare = event['queryStringParameters']['id']
        response = tabellaListaGare.query(KeyConditionExpression=Key('ID').eq(idDaCercare))
        
        
        if response['Items']:
            linkFile = response['Items'][0].get('linkFileGara')
            pathName = linkFile.replace('s3://xmlresults/', '')
            objectFile = s3Client.get_object(Bucket = bucketName, Key = pathName)
            contentXml = base64.b64decode(objectFile['Body'].read())
        else:
            contentXml = 'ID non valido'
            
            
        return{
            'statusCode' : 200,
            'headers': {
              'Content-Type': 'application/xml',
            },
            'body' : contentXml
        }
    except KeyError:
        return{
            'statusCode' : 200,
            'body' : 'nessun parametro id trovato '
        }
    
