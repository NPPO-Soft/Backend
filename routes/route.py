from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from Backend.database.mongo_database import mongo_manager

# Create a Blueprint for routes
main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/dashboard", methods=["GET", "POST"])
def add_document():
    """Add a document to a selected collection via a dashboard-like page."""
    # Get list of collections in the database
    collections = mongo_manager.db.list_collection_names()

    if request.method == "POST":
        # Handle form submission
        selected_collection = request.form.get("collection")
        data = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "department": request.form.get("department"),
        }

        # Insert data into the selected collection
        collection = mongo_manager.get_collection(selected_collection)
        result = collection.insert_one(data)

        # After insertion, redirect to the selected collection's dashboard (or show success message)
        return redirect(url_for("main_routes.collection_dashboard", collection_name=selected_collection))

    return render_template("add_document.html", collections=collections)

@main_routes.route("/collections", methods=["GET"])
def get_collections():
    """Retrieve all collections from the database and render collection selection page."""
    database = mongo_manager.get_database("BS_Database")
    collections = database.list_collection_names()
    
    # Log collections to ensure they are fetched
    print(f"Collections: {collections}")  # Debugging line
    
    return render_template("select_collection.html", collections=collections)

@main_routes.route("/collections/<collection_name>", methods=["GET"])
def collection_dashboard(collection_name):
    """Render the dashboard page for a specific collection."""
    database = mongo_manager.get_database("BS_Database")
    collection = database[collection_name]
    documents = collection.find()  # Retrieve all documents in the collection

    # Remove the '_id' field from each document
    documents_list = [{key: value for key, value in document.items() if key != '_id'} for document in documents]

    return render_template('collection_dashboard.html', collection_name=collection_name, documents=documents_list)