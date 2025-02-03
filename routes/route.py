from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from Backend.database.mongo_database import mongo_manager
import base64
import logging
from bson import ObjectId

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

@main_routes.route("/testimonials", methods=["GET"])
def get_testimonials():
    """Retrieve all testimonials and render the testimonials page."""
    try:
        collection = mongo_manager.get_collection("testimonials")
        testimonials = list(collection.find())

        # Convert `_id` to string for template rendering
        for testimonial in testimonials:
            testimonial["_id"] = str(testimonial["_id"])

        return render_template("testimonials.html", testimonials=testimonials)

    except Exception as e:
        return render_template("testimonials.html", testimonials=[], error_message="Error fetching testimonials.")
    
@main_routes.route("/testimonials/add", methods=["POST"])
def add_testimonial():
    """Add a new testimonial with image stored as Base64."""
    try:
        name = request.form.get("name")
        text = request.form.get("text")
        image = request.files.get("image")

        # Ensure all fields are provided
        if not name or not text or not image:
            return redirect(url_for("main_routes.get_testimonials"))

        # Convert image to Base64
        image_data = base64.b64encode(image.read()).decode("utf-8")

        # Insert into MongoDB
        collection = mongo_manager.get_collection("testimonials")
        collection.insert_one({
            "name": name,
            "text": text,
            "image": f"data:{image.content_type};base64,{image_data}"  # Format Base64 as data URL
        })

        return redirect(url_for("main_routes.get_testimonials"))

    except Exception as e:
        return redirect(url_for("main_routes.get_testimonials"))

@main_routes.route("/testimonials/delete/<string:testimonial_id>", methods=["POST"])
def delete_testimonial(testimonial_id):
    """Delete a testimonial by ID."""
    try:
        collection = mongo_manager.get_collection("testimonials")
        result = collection.delete_one({"_id": ObjectId(testimonial_id)})

        if result.deleted_count == 0:
            return redirect(url_for("main_routes.get_testimonials"))

        return redirect(url_for("main_routes.get_testimonials"))

    except Exception as e:
        return redirect(url_for("main_routes.get_testimonials"))

@main_routes.route("/api/testimonials", methods=["GET"])
def api_get_testimonials():
    """Retrieve all testimonials and return as JSON for the frontend."""
    try:
        collection = mongo_manager.get_collection("testimonials")
        testimonials = list(collection.find())

        # Convert `_id` to string for JSON compatibility
        for testimonial in testimonials:
            testimonial["_id"] = str(testimonial["_id"])

        return jsonify({"success": True, "testimonials": testimonials}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
@main_routes.route("/teams", methods=["GET"])
def get_teams():
    """Retrieve all team members and render the teams page."""
    collection = mongo_manager.get_collection("teams")
    members = list(collection.find())

    for member in members:
        member["_id"] = str(member["_id"])

    return render_template("teams.html", team_members=members)

@main_routes.route("/teams/add", methods=["POST"])
def add_team_member():
    """Add a new team member with image stored as Base64."""
    try:
        name = request.form.get("name")
        department = request.form.get("department")
        image = request.files.get("image")

        if not name or not department or not image:
            return redirect(url_for("main_routes.get_teams"))

        # Convert image to Base64
        image_data = base64.b64encode(image.read()).decode("utf-8")

        # Insert into MongoDB
        collection = mongo_manager.get_collection("teams")
        collection.insert_one({
            "name": name,
            "department": department,
            "image": f"data:{image.content_type};base64,{image_data}"
        })

        return redirect(url_for("main_routes.get_teams"))

    except Exception as e:
        return redirect(url_for("main_routes.get_teams"))

@main_routes.route("/teams/delete/<string:member_id>", methods=["POST"])
def delete_team_member(member_id):
    """Delete a team member by ID."""
    try:
        collection = mongo_manager.get_collection("teams")
        collection.delete_one({"_id": ObjectId(member_id)})
        return redirect(url_for("main_routes.get_teams"))

    except Exception as e:
        return redirect(url_for("main_routes.get_teams"))
    
@main_routes.route("/api/teams", methods=["GET"])
def api_get_tems():
    """Retrieve all teams and return as JSON for the frontend."""
    try:
        collection = mongo_manager.get_collection("teams")
        teams = list(collection.find())

        # Convert `_id` to string for JSON compatibility
        for team in teams:
            team["_id"] = str(team["_id"])

        return jsonify({"success": True, "teams": teams}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500



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

        # Add an empty "Interview" structure
        data["Interview"] = {
            "date": "No date set",
            "hour": "No hour set",
            "location": "No location set"
        }

        # Insert into MongoDB
        collection = mongo_manager.get_collection("recruitments")
        collection.insert_one(data)

        return jsonify({"success": True, "message": "Application submitted successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    
@main_routes.route("/api/interview", methods=["GET"])
def check_interview():
    """Check if a user has an interview date, hour, and location."""
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

        # If user exists, check if interview details are set
        if user:
            interview = user.get("Interview", {})
            interview_date = interview.get("date", "No date set")
            interview_hour = interview.get("hour", "No hour set")
            interview_location = interview.get("location", "No location set")

            return jsonify({
                "success": True,
                "interview": {
                    "date": interview_date,
                    "hour": interview_hour,
                    "location": interview_location
                }
            }), 200

        else:
            return jsonify({"success": False, "message": "User not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@main_routes.route("/recruitments", methods=["GET"])
def get_recruitments():
    try:
        collection = mongo_manager.get_collection("recruitments")
        recruitments = list(collection.find())

        if not recruitments:
            logging.warning("No recruitments found in the database!")

        # Convert _id to string and restructure Interview data
        for recruitment in recruitments:
            recruitment["_id"] = str(recruitment["_id"])  # Ensure _id is a string

            # Ensure Interview field exists and is a dictionary
            if "Interview" not in recruitment or not isinstance(recruitment["Interview"], dict):
                recruitment["Interview"] = {
                    "date": "No date set",
                    "hour": "No hour set",
                    "location": "No location set"
                }
            else:
                # Fill missing fields with default values
                recruitment["Interview"].setdefault("date", "No date set")
                recruitment["Interview"].setdefault("hour", "No hour set")
                recruitment["Interview"].setdefault("location", "No location set")

            logging.info(f"Recruitment Data: {recruitment}")  # Debugging output

        return render_template(
            "recruitments.html",
            recruitments=recruitments,
            fields=[
                "nume",
                "prenume",
                "email",
                "facultate",
                "anUniversitar",
                "motivatie",
                "Interview"
            ]
        )

    except Exception as e:
        logging.error(f"Error fetching recruitments: {e}")
        return render_template(
            "recruitments.html",
            recruitments=[],
            fields=[],
            error_message="There was an error fetching the recruitment applications."
        )

        
from flask import request, redirect, url_for, jsonify
from bson import ObjectId

@main_routes.route('/set_interview_date', methods=['POST'])
def set_interview_date():
    applicant_id = request.form.get('applicant_id')
    new_date = request.form.get('interview_date')
    new_hour = request.form.get('interview_hour')
    new_location = request.form.get('interview_location')

    # Ensure required fields are provided
    if not all([new_date, new_hour, new_location]):
        return redirect(url_for('main_routes.get_recruitments'))  # Redirect with no message

    # Convert `applicant_id` to ObjectId if necessary
    try:
        object_id = ObjectId(applicant_id)
    except Exception:
        return redirect(url_for('main_routes.get_recruitments'))  # Redirect if invalid ID

    # Fetch the applicant from the database
    collection = mongo_manager.get_collection("recruitments")
    applicant = collection.find_one({"_id": object_id})

    if not applicant:
        return redirect(url_for('main_routes.get_recruitments'))  # Redirect if applicant not found

    # Update interview details
    collection.update_one(
        {"_id": object_id}, 
        {"$set": {
            "Interview.date": new_date,
            "Interview.hour": new_hour,
            "Interview.location": new_location
        }}
    )

    return redirect(url_for('main_routes.get_recruitments'))  # Redirect after successful update

