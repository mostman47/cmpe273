# -*- coding: utf-8 -*-
import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    # Your code goes here!
    menu_id = event['menu_id']
    
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('Menu')
    
    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    
    
    response = table.query(
        KeyConditionExpression=Key('menu_id').eq(menu_id),
        Limit=1
    )
    
    jsonObject = json.loads(response['Items'][0]['body'])
    
    for updateKey in event['update']:
        if(updateKey != 'menu_id'):
            print updateKey
            jsonObject[updateKey] =  event['update'][updateKey]
    
    print jsonObject
    #print jsonObject['selection']
     
    #print response;
    
    response = table.update_item(
        Key={
            'menu_id': menu_id
        },
        UpdateExpression="set body = :r",
        ExpressionAttributeValues={
            ':r': json.dumps(jsonObject)
        },
        ReturnValues="UPDATED_NEW"
    )
    
    print("UpdateItem succeeded:")
    print(response)
    return json.loads(response['Attributes']['body']);
