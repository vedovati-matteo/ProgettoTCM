import json
import boto3
import uuid

def lambda_handler(event, context):
    
    try:
        userId = event['headers']['userid']
        raceName = event['queryStringParameters']['race_name']
        raceDate = event['queryStringParameters']['race_date']
        
        # TODO generate raceId and save data in db
        # generate unique id
        raceId = str(uuid.uuid4().hex)
        
        db = boto3.client('dynamodb')
        
        db.put_item(
            TableName = 'ListaGare',
            Item = {
                'ID' : { 'S' : raceId},
                'nomegara' : { 'S' : raceName},
                'DataInizio' : { 'S' : raceDate},
                'ID_gestore' : { 'S' : userId}
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                "race_id": raceId
            })
        }
        
    except KeyError:
        no = "params error"
        return {
            'statusCode': 200,
            'body': "Parms Error"
        }