from flask import Flask, request

app = Flask(__name__)

# initial state
products = [
    {'id': 1, 'name': 'Apple', 'price': 0.5, 'quantity': 50},
    {'id': 2, 'name': 'Banana', 'price': 0.4, 'quantity': 40},
    {'id': 3, 'name': 'Orange', 'price': 0.6, 'quantity': 60},
    {'id': 4, 'name': 'Mango', 'price': 1.0, 'quantity': 30},
]

orders = []

@app.route('/products', methods=['GET'])
def get_products():
    return {'products': products}

@app.route('/orders', methods=['GET'])
def get_orders():
    return {'orders': orders}

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json['order']
    order_id = len(orders) + 1
    orders.append({'id': order_id, 'order': order})
    return {'order_id': order_id}

if __name__ == '__main__':
    app.run()
