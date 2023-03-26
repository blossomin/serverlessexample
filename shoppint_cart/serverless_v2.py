import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('shopping_cart')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_cart(event, context)
    elif http_method == 'POST':
        return add_item(event, context)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

def get_cart(event, context):
    response = table.scan()
    items = response['Items']
    cart = {}
    for item in items:
        cart[item['item']] = item['quantity']
    return {
        'statusCode': 200,
        'body': json.dumps({'cart': cart})
    }

def add_item(event, context):
    item = event['body-json']['item']
    quantity = event['body-json']['quantity']

    # update the DynamoDB table
    table.update_item(
        Key={'item': item},
        UpdateExpression='SET quantity = if_not_exists(quantity, :start) + :inc',
        ExpressionAttributeValues={
            ':start': 0,
            ':inc': quantity
        }
    )

    # return the updated cart
    response = table.scan()
    items = response['Items']
    cart = {}
    for item in items:
        cart[item['item']] = item['quantity']
    return {
        'statusCode': 200,
        'body': json.dumps({'cart': cart})
    }
