import os
import certifi
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    ca = certifi.where()
    client = MongoClient(os.environ.get("MONGODB_URI"), tlsCAFile=ca)
    app.db = client.get_default_database()
    
    app.register_blueprint(pages)
    return app







        




    
   