from flask import Blueprint
from flask_restx import Api, Resource
from flaskr.db import get_db
from datetime import datetime

bp = Blueprint('api', __name__)
wtlfcal = Api(bp)
