import json
import os

DB_FILE = 'products.json'

def init_db():
    """Create products.json if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)
    print("JSON storage ready")

def add_product(name, qty, price, ptype):
    """Add a product to the JSON file."""
    products = get_all_products()
    products.append({
        'name': name,
        'qty': qty,
        'price': price,
        'type': ptype
    })
    with open(DB_FILE, 'w') as f:
        json.dump(products, f, indent=2)
    print(f" Product added: {name} ({ptype})")

def get_all_products():
    """Return all products from the JSON file."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def reset_products():
    """Delete all products (empty the JSON file)."""
    with open(DB_FILE, 'w') as f:
        json.dump([], f)
    print("All products reset")