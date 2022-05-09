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
    
    try:
        userId = event['headers']['userid']
        raceId = event['queryStringParameters']['race_id']
        body = event["body"]
        
        # get both encoded and decode body
        if "isBase64Encoded" in event and event["isBase64Encoded"]:
            XMLencode = body
            stringXML = base64.b64decode(body)
        else:
            stringXML = body
            XMLencode = base64.b64encode(bytes(body, 'utf-8'))
        
        # validate XML
        if validaXML(stringXML, xsdfile):
            print("VALIDO")
            returnStr = upload(bucketName, userId, raceId, stringXML, XMLencode)
        else:
            print("INVALIDO")
            returnStr = "formato XML non valido"
            
        return{
            'statusCode' : 200,
            'body' : returnStr
        }
        
    except KeyError:    
        return{
            'statusCode' : 200,
            'body' : 'Parms Error'
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

def upload(bucketName, userId, raceId, stringXML, XMLencode):
    db = boto3.client('dynamodb')
    s3 = boto3.resource('s3')
    
    pathName = 'results/'+raceId+'.xml'
    
    rootTree = ET.fromstring(stringXML)
    ns = get_namespace(rootTree)
    eventTree = rootTree.find(ns+'Event')
    
    tabellaListaGare = boto3.resource('dynamodb').Table('ListaGare')
    response = tabellaListaGare.query(KeyConditionExpression=Key('ID').eq(raceId))

    strReturn = ""

    if response['Items']: # check if race exist
        
        gara = response['Items'][0]
        gestoreID = gara.get('ID_gestore')
        
        if (gestoreID == userId): # check if user can update race 
            
            if not gara.get('Stato'): # check if file can be updated
                
                endTimeTree = eventTree.find(ns+'EndTime')
                
                if 'linkFileGara' in gara: # check if race has already an XML uploaded
                
                    if endTimeTree is None: # check if is last update
                        
                        strReturn = "File XML aggirnato"
                        stato = False
                        
                        db.update_item(
                            TableName='ListaGare',
                            Key={
                                'ID': { 'S' : raceId}
                            },
                            UpdateExpression='SET Stato = :s',
                            ExpressionAttributeValues={
                                ':s': { 'BOOL' : stato}
                            }
                        )
                        
                    else: # last update
                        
                        strReturn = "File XML aggirnato e non più modificabile"
                        stato = True
                        oraFine = eventTree.find(ns+'EndTime').find(ns+'Time').text
                        
                        db.update_item(
                            TableName='ListaGare',
                            Key={ 
                                'ID': { 'S' : raceId}
                            },
                            UpdateExpression='SET OraFine = :oF, Stato = :s',
                            ExpressionAttributeValues={
                                ':oF': { 'S' : oraFine},
                                ':s': { 'BOOL' : stato}
                            }
                        )
                    
                else: # first time uploading
                    url = 's3://xmlresults/'+pathName
                    oraInizio = eventTree.find(ns+'StartTime').find(ns+'Time').text
                    
                    if endTimeTree is None:
                        strReturn = "File XML aggiunto"
                        stato = False

                        db.update_item(
                            TableName='ListaGare',
                            Key={ 
                                'ID': { 'S' : raceId}
                            },
                            UpdateExpression='SET linkFileGara = :fg, OraInizio = :oI, Stato = :s',
                            ExpressionAttributeValues={
                                ':fg': { 'S' : url},
                                ':oI': { 'S' : oraInizio},
                                ':s': { 'BOOL' : stato}
                            }
                        )
                    else:
                        strReturn = "File XML aggiunto e non più modificabile"
                        stato = True
                        oraFine = eventTree.find(ns+'EndTime').find(ns+'Time').text

                        db.update_item(
                            TableName='ListaGare',
                            Key={ 
                                'ID': { 'S' : raceId}
                            },
                            UpdateExpression='SET linkFileGara = :fg, OraInizio = :oI, OraFine = :oF, Stato = :s',
                            ExpressionAttributeValues={
                                ':fg': { 'S' : url},
                                ':oI': { 'S' : oraInizio},
                                ':oF': { 'S' : oraFine},
                                ':s': { 'BOOL' : stato}
                            }
                        )

                # upload file to bucket
                s3.Bucket(bucketName).put_object(Key = pathName, Body = XMLencode)

            else:
                strReturn = "File XML non aggirnato perché non più modificabile"
            
        else:
            strReturn = "L'utente non è il gestore della gara"
    
    else:
        strReturn = "La gara di id:" + raceId + " non esiste"
    
    return strReturn