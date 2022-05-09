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
        
        splittedLink = pathSplitter(linkXML)
    
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket = splittedLink['bucketName'], Key = splittedLink['path_relative'])
        content = base64.b64decode(response['Body'].read())
        
        if 'class' in event['queryStringParameters']:
            param_class = event['queryStringParameters']['class']
            
            placement = getPlacement(content, param_class)
            if placement == None:
                return {
                    'statusCode' : 200,
                    'body' : 'nessuna categoria trovata con questo id'
                }
            else:
                return {
                    'statusCode' : 200,
                    'body' : json.dumps(placement)
                }
            
        elif 'organisation' in event['queryStringParameters']:
            param_organization = event['queryStringParameters']['organisation']
            
            organization = getOrganisation(content, param_organization)
    
            return {
                'statusCode' : 200,
                'body' : json.dumps(organization)
            }
            
        else:
            raise KeyError('class or organisation no present')
            
        
    except KeyError:
        return {
            'statusCode' : '200',
            'body' : 'parametri sbagliati'
        }



def getOrganisation(xmlstring, param_organization):
    root = ET.fromstring(xmlstring)
    ns = get_namespace(root)
    people = []
    for cr in root.findall(ns + 'ClassResult'):
        for pr in cr.findall(ns + 'PersonResult'):
            if(pr.find(ns + 'Organisation').find(ns + 'Id').text == param_organization):
                persona = pr.find(ns + 'Person')
                nome = persona.find (ns + 'Name')
                item = {
                    'id' :persona.find(ns + 'Id').text,
                    'family' : nome.find(ns + 'Family').text,
                    'given' : nome.find(ns + 'Given').text,
                }
                people.append(item)
    return people

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

def makeItem(personResult, ns):     #tested
    person = personResult.find(ns + 'Person')
    name = person.find(ns + 'Name')
    result = personResult.find(ns + 'Result')

    time = result.find(ns + 'Time')
    if time == None:
        time = -1
    else:
        time = time.text

    position = result.find(ns + 'Position')
    if position == None:
        position = -1
    else:
        position = position.text


    status = result.find(ns + 'Status')
    if status == None:
        status = "no status given"
    else:
        status = status.text

    item = {
        'id' : person.find(ns + 'Id').text,
        'family' : name.find(ns + 'Family').text,
        'given' : name.find(ns + 'Given').text,
        'time' : time,
        'position' : position,
        'status' : status
    }
    return item

def getPlacement(xmlstring, param_class):   #tested

    root = ET.fromstring(xmlstring)
    ns = get_namespace(root)
    placement = []


    for classresult in root.findall(ns + 'ClassResult'):
        ids = classresult.find(ns + 'Class').find(ns + 'Id').text
        if ids == param_class:
            for r in classresult.findall(ns + 'PersonResult'):
                placement.append(makeItem(r, ns))
    return placement