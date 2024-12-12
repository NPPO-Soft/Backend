import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoManager:
    def __init__(self):
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster_url = os.getenv("MONGODB_CLUSTER_URL")
        self.client = MongoClient(
            f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
        )
        self.db = self.client.get_database("BS_Database")  

    def get_collection(self, collection_name):
        """Return a specific collection."""
        return self.db[collection_name]
    
    def get_database(self, db_name):
        """Retrieve the database by name."""
        return self.client[db_name]
    

mongo_manager = MongoManager()