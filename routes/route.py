from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from Backend.database.mongo_database import mongo_manager
import base64

# Create a Blueprint for routes
main_routes = Blueprint("main_routes", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_routes.route("/", methods=["GET"])
def index():
    """Render the home page with navigation buttons."""
    return render_template("index.html")

@main_routes.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Handle adding documents and uploading images."""
    # Get list of collections in the database
    collections = mongo_manager.db.list_collection_names()

    # Filter out system collections (those starting with "system.")
    collections = [collection for collection in collections if not collection.startswith('system.')]

    if request.method == "POST":
        # Determine which form was submitted
        if "add_document" in request.form:
            # Handle document addition
            selected_collection = request.form.get("collection")
            data = {
                "name": request.form.get("name"),
                "age": request.form.get("age"),
                "department": request.form.get("department"),
            }
            # Insert data into the selected collection
            collection = mongo_manager.get_collection(selected_collection)
            collection.insert_one(data)
            return redirect(url_for("main_routes.dashboard", collection_name=selected_collection))

        elif "upload_image" in request.form:
            # Handle image upload
            if "image" in request.files:
                uploaded_file = request.files["image"]
                if uploaded_file.filename != "":
                    if allowed_file(uploaded_file.filename):
                        # Directly use the original filename
                        original_filename = uploaded_file.filename
                        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

                        # Save image to the "images" collection in the database
                        collection = mongo_manager.get_collection("images")
                        collection.insert_one({
                            "filename": original_filename,
                            "content": image_data
                        })
                        return "Image uploaded successfully!", 200
                    else:
                        return "Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.", 400
            return "No image uploaded.", 400

    return render_template("dashboard.html", collections=collections)


@main_routes.route("/collections", methods=["GET", "POST"])
def get_collections():
    """Retrieve all collections from the database and render collection selection page."""
    collections = mongo_manager.db.list_collection_names()

    # Filter out system collections
    collections = [collection for collection in collections if not collection.startswith('system.')]

    selected_collection = None
    documents = []

    if request.method == "POST":
        selected_collection = request.form.get("selected_collection")
        if selected_collection:
            collection = mongo_manager.get_collection(selected_collection)
            documents_cursor = collection.find()  # Retrieve all documents in the collection

            # Remove the '_id' field from each document
            documents = [{key: value for key, value in document.items() if key != '_id'} for document in documents_cursor]

    return render_template("select_collection.html", collections=collections, selected_collection=selected_collection, documents=documents)


@main_routes.route("/api/collections", methods=["GET", "POST"])
def get_collections_api():
    """Retrieve all collections from the database and return them as JSON."""
    collections = mongo_manager.db.list_collection_names()

    # Filter out system collections
    collections = [collection for collection in collections if not collection.startswith('system.')]

    if request.method == "POST":
        selected_collection = request.json.get("selected_collection")
        documents = []

        if selected_collection:
            collection = mongo_manager.get_collection(selected_collection)
            documents_cursor = collection.find()  # Retrieve all documents in the collection

            # Remove the '_id' field from each document
            documents = [{key: value for key, value in document.items() if key != '_id'} for document in documents_cursor]

        response = {
            "documents": documents
        }
        return jsonify(response)

    # GET method to return collections
    response = {
        "collections": collections
    }

    return jsonify(response)

@main_routes.route("/api/recrutari", methods=["POST"])
def submit_recruitment():
    """Endpoint to handle recruitment form submissions."""
    try:
        # Get JSON data from request
        data = request.json

        # Validate required fields
        required_fields = ["nume", "prenume", "email", "facultate", "anUniversitar", "motivatie"]
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Validate email format
        if "@" not in data["email"]:
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        # Add an empty "Interview" field to the data
        data["Interview"] = ""  # This field will be empty initially

        # Insert into MongoDB
        collection = mongo_manager.get_collection("recruitments")
        collection.insert_one(data)

        return jsonify({"success": True, "message": "Application submitted successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
@main_routes.route("/api/interview", methods=["GET"])
def check_interview():
    """Check if a user has an interview date."""
    try:
        # Get parameters from request
        nume = request.args.get("nume")
        prenume = request.args.get("prenume")
        facultate = request.args.get("facultate")
        anUniversitar = request.args.get("anUniversitar")

        # Validate required fields
        if not all([nume, prenume, facultate, anUniversitar]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Connect to MongoDB and find user
        collection = mongo_manager.get_collection("recruitments")
        user = collection.find_one({
            "nume": nume,
            "prenume": prenume,
            "facultate": facultate,
            "anUniversitar": anUniversitar
        })

        # If user exists, check if an interview date is set
        if user:
            interview_date = user.get("Interview", "")

            if interview_date:
                return jsonify({
                    "success": True,
                    "interview": interview_date
                }), 200
            else:
                return jsonify({
                    "success": True,
                    "interview": "No interview date set yet."
                }), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


