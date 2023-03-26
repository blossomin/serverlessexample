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

def update_product(event, context):
    product_id = event['pathParameters']['id']
    product = event['body-json']['product']
    response = table.update_item(
        Key={'id': product_id},
        UpdateExpression='SET #n = :name, #p = :price, #q = :quantity',
        ExpressionAttributeNames={'#n': 'name', '#p': 'price', '#q': 'quantity'},
        ExpressionAttributeValues={':name': product['name'], ':price': product['price'], ':quantity': product['quantity']},
        ReturnValues='UPDATED_NEW'
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'product': response['Attributes']})
    }
