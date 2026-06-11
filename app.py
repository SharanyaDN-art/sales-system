from flask import Flask, render_template, request, jsonify
from abc import ABC, abstractmethod
import db

app = Flask(__name__)

#abstraction and encapsulation
class Product(ABC):
    def __init__(self, name, qty, price):
        self._name = name
        self._qty = qty
        self._price = price

    @abstractmethod
    def total(self):
        pass

    def to_dict(self):
        return {
            "name": self._name,
            "qty": self._qty,
            "price": self._price,
            "total": self.total()
        }
#inheritance
class PhysicalProduct(Product):
    def total(self):
        return self._qty * self._price

class DigitalProduct(Product):
    def total(self):
        return (self._qty * self._price) * 0.5
#ploymorphism
class SalesSystem:
    def __init__(self):
        pass

    def add_product(self, product):
        ptype = 'digital' if isinstance(product, DigitalProduct) else 'physical'
        db.add_product(product._name, product._qty, product._price, ptype)

    def get_all_products(self):
        rows = db.get_all_products()
        products = []
        for row in rows:
            if row['type'] == 'digital':
                prod = DigitalProduct(row['name'], row['qty'], row['price'])
            else:
                prod = PhysicalProduct(row['name'], row['qty'], row['price'])
            products.append(prod.to_dict())
        return products

    def reset(self):
        db.reset_products()

system = SalesSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(system.get_all_products())

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    qty = int(data.get('qty', 0))
    price = float(data.get('price', 0))
    ptype = data.get('type', 'physical')
    if ptype == 'digital':
        product = DigitalProduct(name, qty, price)
    else:
        product = PhysicalProduct(name, qty, price)
    system.add_product(product)
    return jsonify({'ok': True})

@app.route('/api/reset', methods=['POST'])
def reset():
    system.reset()
    return jsonify({'ok': True})

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True, port=5001)