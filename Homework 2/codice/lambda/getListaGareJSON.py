import json
import boto3

def lambda_handler(event, context):
    bucketName = 'xmlresults'
    s3 = boto3.resource('s3')
    tabellaListaGare = boto3.resource('dynamodb').Table('ListaGare')
    
    response = tabellaListaGare.scan()
    
    if response['Count'] > 0:
        data = response['Items']
        output = []
        for item in data:
            dict = {}
            dict['ID'] = item['ID']
            dict['NomeGara'] = item['nomegara']
            dict['DataInizio'] = item['DataInizio']
            if 'OraInizio' in item:
                dict['OraInizio'] = item['OraInizio']
            if 'OraFine' in item:
                dict['OraFine'] = item['OraFine']
            output.append(dict)
            
        listaJson = json.dumps(output)
        
    else:
        listaJson = 'Non ci sono gare'
    
    return{
        'statusCode' : 200,
        'headers': {
          'Content-Type': 'application/json',
        },
        'body' : listaJson
    }