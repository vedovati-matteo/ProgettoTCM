import boto3
import json
from boto3.dynamodb.conditions import Key
import xml.etree.ElementTree as ET
import re
import base64


def lambda_handler(event, context):
    try:
        param_id = event['queryStringParameters']['id']
        
        #parte per prendere il file
        linkXML = boto3.resource('dynamodb').Table('ListaGare').get_item(
                Key={
                    'ID' : param_id
                }
        )['Item'].get('linkFileGara')
        
        if (linkXML == None):
            return {
                'statusCode' : '200',
                'body' : ''
            }
        
        splittedLink = pathSplitter(linkXML)
    
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket = splittedLink['bucketName'], Key = splittedLink['path_relative'])
        
        content = base64.b64decode(response['Body'].read())
        return {
            'statusCode' : 200,
            'body' : json.dumps(getOrganisations(content))
        }
    except KeyError:
        return {
            'statusCode' : '200',
            'body' : 'nessun parametro id trovato'
        }
    
    



def getOrganisations(xmlstring):
    root = ET.fromstring(xmlstring)
    ns = get_namespace(root)
    organisations = []
    for cr in root.findall(ns + 'ClassResult'):
        for pr in cr.findall(ns + 'PersonResult'):
            org = pr.find(ns + 'Organisation')
            if org != None and org.find(ns + 'Id') != None and org.find(ns + 'Name') != None:
                temp = {
                    'id' : org.find(ns+'Id').text,
                    'name' : org.find(ns + 'Name').text
                }
                if temp not in organisations:
                    organisations.append(temp)
    return organisations

def get_namespace(element): #tested
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def pathSplitter(path): #tested
    stringspl = path.split('/')
    s = ""
    bucketName = stringspl[2]
    for a in stringspl[3:-1]:
        s = s + a + '/'
    s = s + stringspl[-1]
    return {
        'bucketName' : bucketName,
        'path_relative' : s
    }
