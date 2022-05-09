import boto3
import json
from boto3.dynamodb.conditions import Key
import xml.etree.ElementTree as ET
import re
import base64

def lambda_handler(event, context):
    try:
        id = event['queryStringParameters']['id']
        
        linkXML = boto3.resource('dynamodb').Table('ListaGare').get_item(
            Key={
                'ID' : id
            }
        )['Item'].get('linkFileGara')
        
        splittedLink = pathSplitter(linkXML)

        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket = splittedLink['bucketName'], Key = splittedLink['path_relative'])
        
        content = base64.b64decode(response['Body'].read())

        return {
            'statusCode' : 200,
            'body' : json.dumps(getClasses(content))
        }
    except KeyError:
        return {
            'statusCode' : '200',
            'body' : 'nessun parametro id trovato'
        }
    

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

def get_namespace(element): #tested
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def getClasses(xmlstring): #tested

    root = ET.fromstring(xmlstring)
    ns = get_namespace(root)


    """categoryList = ""

    for classresult in root.findall(ns + 'ClassResult'):
        f = classresult.find(ns + 'Class')
        categoryList = categoryList + "Id: " + f.find(ns + 'Id').text + "\tCategoria: " + f.find(ns + 'Name').text + '\n'"""
    
    

    #sopra è in formato stringa, ora faccio con JSON
    categoryList = []
    for classresult in root.findall(ns + 'ClassResult'):
        f = classresult.find(ns + 'Class')
        item = {
            "id" : f.find(ns + 'Id').text,
            "class" : f.find(ns + 'Name').text
        }
        categoryList.append(item)
    return categoryList