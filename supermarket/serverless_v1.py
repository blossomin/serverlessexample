import json

def get_products(event, context):
    products = [
        {'id': 1, 'name': 'Apple', 'price': 0.5, 'quantity': 50},
        {'id': 2, 'name': 'Banana', 'price': 0.4, 'quantity': 40},
        {'id': 3, 'name': 'Orange', 'price': 0.6, 'quantity': 60},
        {'id': 4, 'name': 'Mango', 'price': 1.0, 'quantity': 30},
    ]
    return {
        'statusCode': 200,
        'body': json.dumps({'products': products})
    }

def get_orders(event, context):
    orders = []
    return {
        'statusCode': 200,
        'body': json.dumps({'orders': orders})
    }

def create_order(event, context):
    order = event['body-json']['order']
    order_id = len(orders) + 1
    orders.append({'id': order_id, 'order': order})
    return {
        'statusCode': 200,
        'body': json.dumps({'order_id': order_id})
    }
