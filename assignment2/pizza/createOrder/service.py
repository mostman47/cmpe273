import boto3
import json
import datetime

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    # Your code goes here!
    customer_name = event['customer_name']
    menu_id = event['menu_id']
    
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table1 = dynamodb.Table('Menu')
    
    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    
    
    response1 = table1.query(
        KeyConditionExpression=Key('menu_id').eq(menu_id),
        Limit=1
    )
    
    body = json.loads(response1['Items'][0]['body'])
    
    message = "Hi %s, please choose one of these selection:  %s"
    
    selections = body['selection']
    str = ""
    for index,key in enumerate(selections):
        str += `(index + 1)` + ". " + key + " "
    print str
    
    table2 = dynamodb.Table('Order')
    
    response = table2.put_item(
       Item={
            'order_id': event['order_id'],
            'menu_id': event['menu_id'],
            'body': event,
            'order_status': 'processing',
            'selection': 'null',
            'size': 'null',
            'costs': 'null',
            'order_time': datetime.datetime.now().strftime("%m-%d-%Y@%H:%M:%S")
        }
    )
    
    
    return {"Message":message % (customer_name,str)}