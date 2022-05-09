import json
import base64
import boto3
import xmlschema
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import uuid
from boto3.dynamodb.conditions import Key
import re

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    xsdfile = 'https://raw.githubusercontent.com/international-orienteering-federation/datastandard-v3/master/IOF.xsd'
    bucketName = 'xmlresults'
    
    body = event["body"]
    if "isBase64Encoded" in event and event["isBase64Encoded"]:
        XMLencode = body
        stringXML = base64.b64decode(body)
    else:
        stringXML = body
        XMLencode = base64.b64encode(bytes(body, 'utf-8'))
    
    
    if validaXML(stringXML, xsdfile):
        print("VALIDO")
        returnStr = upload(bucketName, stringXML, XMLencode)
    else:
        print("INVALIDO")
        returnStr = "formato XML non valido"

    return{
        'statusCode' : 200,
        'body' : returnStr
    }


def get_namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def validaXML(xmlstring, xsdfile):
    error = False
    try:
        xmlschema.validate(xmlstring, xsdfile)
    except:
        error = True
    else:
        #passata validazione con xsd
        root = ET.fromstring(xmlstring)
        #print(root)

        ns = get_namespace(root)

        root = root.tag
        firstElement = root[len(ns):]
        #print(firstElement)

        if firstElement != "ResultList":
            error = True

    return not(error)

def upload(bucketName, stringXML, XMLencode):
    db = boto3.client('dynamodb')
    s3 = boto3.resource('s3')
    
    nID = uuid.uuid4().hex
    pathName = 'results/'+nID+'.xml'
    
    rootTree = ET.fromstring(stringXML)
    ns = get_namespace(rootTree)
    eventTree = rootTree.find(ns+'Event')
    nomeGaraDaCercare = eventTree.find(ns+'Name').text
    
    tabellaListaGare = boto3.resource('dynamodb').Table('ListaGare')
    response = tabellaListaGare.query(KeyConditionExpression=Key('NomeGara').eq(nomeGaraDaCercare))

    strReturn = ""

    #Controllo se il file esiste
    if response['Items']:
        nID = response['Items'][0].get('ID')
        pathName = 'results/'+nID+'.xml'
        if not response['Items'][0].get('Stato'):
            endTimeTree = eventTree.find(ns+'EndTime')
            if endTimeTree is None:
                strReturn = "File XML aggirnato"
                stato = False
                db.update_item(
                    TableName='ListaGare',
                    Key={ 
                        'NomeGara': { 'S' : nomeGaraDaCercare},
                        'ID': { 'S' : nID}
                    },
                    UpdateExpression='SET Stato = :s',
                    ExpressionAttributeValues={
                        ':s': { 'BOOL' : stato}
                    }
                )
            else:
                strReturn = "File XML aggirnato e non più modificabile"
                stato = True
                dataFine = eventTree.find(ns+'EndTime').find(ns+'Date').text
                oraFine = eventTree.find(ns+'EndTime').find(ns+'Time').text
                db.update_item(
                    TableName='ListaGare',
                    Key={ 
                        'NomeGara': { 'S' : nomeGaraDaCercare},
                        'ID': { 'S' : nID}
                    },
                    UpdateExpression='SET DataFine = :dF, OraFine = :oF, Stato = :s',
                    ExpressionAttributeValues={
                        ':dF': { 'S' : dataFine},
                        ':oF': { 'S' : oraFine},
                        ':s': { 'BOOL' : stato}
                    }
                )
        else:
            strReturn = "File XML non aggirnato perché non più modificabile"
    else:
        url = 's3://xmlresult/'+pathName
        dataInizio = eventTree.find(ns+'StartTime').find(ns+'Date').text
        oraInizio = eventTree.find(ns+'StartTime').find(ns+'Time').text
        endTimeTree = eventTree.find(ns+'EndTime')
        nomeGara = eventTree.find(ns+'Name').text
        if endTimeTree is None:
            strReturn = "File XML aggiunto"
            stato = False
            db.put_item(
                TableName = 'ListaGare',
                Item = {
                    'NomeGara' : { 'S' : nomeGara},
                    'ID' : { 'S' : nID},
                    'linkFileGara' : { 'S' : url},
                    'DataInizio' : { 'S' : dataInizio},
                    'OraInizio' : { 'S' : oraInizio},
                    'Stato' : { 'BOOL' : stato}
             }
        )
        else:
            strReturn = "File XML aggiunto e non più modificabile"
            stato = True
            dataFine = eventTree.find(ns+'EndTime').find(ns+'Date').text
            oraFine = eventTree.find(ns+'EndTime').find(ns+'Time').text
            db.put_item(
                TableName = 'ListaGare',
                Item = {
                    'NomeGara' : { 'S' : nomeGara},
                    'ID' : { 'S' : nID},
                    'linkFileGara' : { 'S' : url},
                    'DataInizio' : { 'S' : dataInizio},
                    'OraInizio' : { 'S' : oraInizio},
                    'DataFine' : { 'S' : dataFine},
                    'OraFine' : { 'S' : oraFine},
                    'Stato' : { 'BOOL' : stato}
             }
        )
        
        

    s3.Bucket(bucketName).put_object(Key = pathName, Body = XMLencode)
    
    return strReturn