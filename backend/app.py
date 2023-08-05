from bson import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['crudApp']
collection = db['dummyData']

ma = Marshmallow(app)

# Data model
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


# Create operation
@app.route('/api/create', methods=['POST'])
def create():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    new_item = Item(name, description)
    collection.insert_one(new_item.__dict__)

    return jsonify({"message": "Item created successfully"})


# Read operation
@app.route('/api/read', methods=['GET'])
def read():
    items = list(collection.find())

    # Convert ObjectId to string for serialization
    for item in items:
        item['_id'] = str(item['_id'])

    return jsonify(items)


# Update operation
@app.route('/api/update/<string:item_id>', methods=['PUT'])
def update(item_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')

    item = collection.find_one_and_update({'_id': ObjectId(item_id)}, {'$set': {'name': name, 'description': description}})
    if item:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "Item not found"}), 404


# Delete operation
@app.route('/api/delete/<string:item_id>', methods=['DELETE'])
def delete(item_id):
    result = collection.delete_one({'_id': ObjectId(item_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "Item not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
