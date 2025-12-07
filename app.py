from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = 'cheltuieli.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"transactions": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    data = load_data()
    return jsonify(data['transactions'])

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    transaction = request.json
    transaction['id'] = datetime.now().isoformat()
    
    data = load_data()
    data['transactions'].append(transaction)
    save_data(data)
    
    return jsonify(transaction), 201

@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    data = load_data()
    data['transactions'] = [t for t in data['transactions'] if t['id'] != transaction_id]
    save_data(data)
    return '', 204

@app.route('/api/summary', methods=['GET'])
def get_summary():
    data = load_data()
    transactions = data['transactions']
    
    total = sum(float(t.get('amount', 0)) for t in transactions)
    by_category = {}
    
    for t in transactions:
        category = t.get('category', 'Altele')
        amount = float(t.get('amount', 0))
        by_category[category] = by_category.get(category, 0) + amount
    
    return jsonify({
        'total': total,
        'by_category': by_category,
        'count': len(transactions)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
