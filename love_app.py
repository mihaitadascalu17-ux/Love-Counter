from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
LOVE_DATA_FILE = 'love_data.json'

def load_love_data():
    if os.path.exists(LOVE_DATA_FILE):
        with open(LOVE_DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Force start date to 5.07.2021
                data['start_date'] = '2021-07-05T00:00:00'
                return data
            except:
                pass
    
    # Create new data with fixed start date
    return {
        "start_date": "2021-07-05T00:00:00",
        "memories": [],
        "initials": "C+M"
    }

def save_love_data(data):
    with open(LOVE_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('love.html')

@app.route('/api/days')
def get_days():
    data = load_love_data()
    start = datetime.fromisoformat(data['start_date'])
    days = (datetime.now() - start).days
    return jsonify({
        'days': days, 
        'start_date': data['start_date']
    })

@app.route('/api/memories', methods=['GET'])
def get_memories():
    data = load_love_data()
    return jsonify(data['memories'])

@app.route('/api/memories', methods=['POST'])
def add_memory():
    memory = request.json
    memory['id'] = datetime.now().isoformat()
    memory['date'] = datetime.now().strftime('%d.%m.%Y')
    
    data = load_love_data()
    data['memories'].append(memory)
    save_love_data(data)
    
    return jsonify(memory), 201

@app.route('/api/memories/<memory_id>', methods=['DELETE'])
def delete_memory(memory_id):
    data = load_love_data()
    data['memories'] = [m for m in data['memories'] if m['id'] != memory_id]
    save_love_data(data)
    return '', 204

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    data = load_love_data()
    
    if request.method == 'POST':
        config = request.json
        data['background_image'] = config.get('background_image', data.get('background_image', ''))
        data['initials'] = config.get('initials', data.get('initials', 'C+M'))
        data['person1_name'] = config.get('person1_name', data.get('person1_name', ''))
        data['person1_photo'] = config.get('person1_photo', data.get('person1_photo', ''))
        data['person2_name'] = config.get('person2_name', data.get('person2_name', ''))
        data['person2_photo'] = config.get('person2_photo', data.get('person2_photo', ''))
        # Keep start_date locked to 2021-07-05
        data['start_date'] = '2021-07-05T00:00:00'
        save_love_data(data)
    
    return jsonify({
        'background_image': data.get('background_image', ''),
        'initials': data.get('initials', 'C+M'),
        'person1_name': data.get('person1_name', ''),
        'person1_photo': data.get('person1_photo', ''),
        'person2_name': data.get('person2_name', ''),
        'person2_photo': data.get('person2_photo', ''),
        'start_date': data['start_date']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
