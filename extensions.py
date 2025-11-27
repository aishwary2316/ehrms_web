"""
Flask extensions initialization.
"""
from flask_pymongo import PyMongo
from flask_login import LoginManager

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
