import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    # Your code goes here!
    order_id = event['order_id']
    input =  event['input']
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table1 = dynamodb.Table('Menu')
    table2 = dynamodb.Table('Order')
    response2 = table2.query(
        KeyConditionExpression=Key('order_id').eq(order_id),
        Limit=1
    )
    
    order = response2['Items'][0]
    menu_id = order['menu_id']
    print menu_id
    
    response1 = table1.query(
        KeyConditionExpression=Key('menu_id').eq(menu_id),
        Limit=1
    )
    
    body = json.loads(response1['Items'][0]['body'])
    
    message = ""
    
    if order['selection'] == 'null':
        table2.update_item(
            Key={
                'order_id': order_id
            },
            UpdateExpression="set selection = :r",
            ExpressionAttributeValues={
                ':r': body['selection'][input - 1]
            },
            ReturnValues="UPDATED_NEW"
        )
        str = ""
        for index,key in enumerate(body['size']):
            str += `(index + 1)` + ". " + key + " "
        print str
        message = { "Message":"Which size do you want? %s" % str}
        
    elif order['size'] == 'null':
        table2.update_item(
            Key={
                'order_id': order_id
            },
            UpdateExpression="set size = :r",
            ExpressionAttributeValues={
                ':r': body['size'][input - 1]
            },
            ReturnValues="UPDATED_NEW"
        )
        
        print body['price']
        
        table2.update_item(
            Key={
                'order_id': order_id
            },
            UpdateExpression="set costs = :r",
            ExpressionAttributeValues={
                ':r': body['price'][input - 1]
            },
            ReturnValues="UPDATED_NEW"
        )
        
        response3 = table2.query(
            KeyConditionExpression=Key('order_id').eq(order_id),
            Limit=1
        )
        
        
        
        tmp = response3['Items'][0]
        
        body2 = tmp['body']
        message = { "Message": "Your order costs %s. We will email you when the order is ready. Thank you!" % tmp['costs']}
        
        # body2['order_status'] = tmp['order_status']
        # body2['order'] = {}
        # body2['order']['selection'] = tmp['selection']
        # body2['order']['size'] = tmp['size']
        # body2['order']['costs'] = tmp['costs']
        # body2['order']['order_time'] = tmp['order_time']
        
        # print body2
        # message = body2
    
    return message