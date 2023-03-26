import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Supermarket'
table = dynamodb.Table(table_name)

def get_products(event, context):
    response = table.scan()
    products = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps({'products': products})
    }

def get_orders(event, context):
    response = table.scan()
    orders = []
    for item in response['Items']:
        orders.append(item['order'])
    return {
        'statusCode': 200,
        'body': json.dumps({'orders': orders})
    }

def create_order(event, context):
    order = event['body-json']['order']
    response = table.scan()
    order_id = len(response['Items']) + 1
    table.put_item(
        Item={
            'id': order_id,
            'order': order
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'order_id': order_id})
    }
