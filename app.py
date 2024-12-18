from flask import Flask
from Backend.routes.route import main_routes  
from Backend.database.mongo_database import mongo_manager  

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.register_blueprint(main_routes)

    try:
        mongo_manager.db.list_collection_names()
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
