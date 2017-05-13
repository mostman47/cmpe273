import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    order_id = event['order_id']
    dynamodb = boto3.resource('dynamodb')
    table2 = dynamodb.Table('Order')
    response2 = table2.query(
        KeyConditionExpression=Key('order_id').eq(order_id),
        Limit=1
    )
    tmp = response2['Items'][0]
    body2 = tmp['body']
    body2['order_status'] = tmp['order_status']
    body2['order'] = {}
    body2['order']['selection'] = tmp['selection']
    body2['order']['size'] = tmp['size']
    body2['order']['costs'] = tmp['costs']
    body2['order']['order_time'] = tmp['order_time']
    
    print body2
    # TODO implement
    return body2