from flask import Blueprint
from flask_restx import Api, Resource
#from flaskr.db import get_db
from datetime import datetime
from instascrape import *

bp = Blueprint('api', __name__)
wtlfcal = Api(bp)

# use pypi insta-scraper and facebook scraper to look through wpc posts and grab data
#seek keywords and print it in Json, display through AJAX
google = Profile('https://www.instagram.com/wpcportugal/?utm_source=ig_embed&hl=en')
google_post = Post('https://www.instagram.com/wpcportugal/?hl=en')

google.scrape()
google_post.scrape()

print(google_post['hashtags'])