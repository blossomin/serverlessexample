from flask import Flask, request

app = Flask(__name__)

# initial state
shopping_cart = {}

@app.route('/cart', methods=['GET'])
def get_cart():
    return {'cart': shopping_cart}

@app.route('/cart', methods=['POST'])
def add_item():
    item = request.json['item']
    quantity = request.json['quantity']

    if item in shopping_cart:
        shopping_cart[item] += quantity
    else:
        shopping_cart[item] = quantity

    return {'cart': shopping_cart}

if __name__ == '__main__':
    app.run()
