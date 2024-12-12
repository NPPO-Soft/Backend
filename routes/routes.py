from flask import Blueprint, jsonify, request
from database.mongo_manager import mongo_manager

# Create a Blueprint for routes
main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/add", methods=["POST"])
def add_document():
    """Add a document to the database."""
    data = request.json
    collection = mongo_manager.get_collection("users") 
    result = collection.insert_one(data)
    return jsonify({"message": "Document added", "id": str(result.inserted_id)}), 201


@main_routes.route("/documents", methods=["GET"])
def get_documents():
    """Retrieve all documents from the database."""
    collection = mongo_manager.get_collection("users")  
    documents = list(collection.find({}, {"_id": 0}))  
    return jsonify(documents)
