from flask import Blueprint
from flask_restx import Api, Resource
from flaskr.db import get_db
from datetime import datetime

bp = Blueprint('api', __name__)
wtlfcal = Api(bp)

# use pypi insta-scraper and facebook scraper to look through wpc posts and grab data
#seek keywords and print it in Json, display through AJAX