from flask import Flask
from routes.routes import main_routes  
from database.mongo_manager import mongo_manager  

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
    app.run(debug=True)
