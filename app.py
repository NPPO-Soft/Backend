from flask import Flask
<<<<<<< HEAD
from Backend.routes.route import main_routes  
from Backend.database.mongo_database import mongo_manager  
=======
from routes.routes import main_routes  
from database.mongo_manager import mongo_manager  
>>>>>>> 3460e82d14719d8dd6f27c8016e4aa7d40b32e1a

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
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> 3460e82d14719d8dd6f27c8016e4aa7d40b32e1a
