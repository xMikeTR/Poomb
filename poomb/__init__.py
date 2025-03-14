import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail

jwt = JWTManager()
mail = Mail()





def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='e582d3a8a64967e1231a9c462e4d90ca9e2cc00217389f593930f88e773fb048',
        DATABASE=os.path.join(app.instance_path, 'poomb.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

   
       
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import log
    app.register_blueprint(log.bp)
    app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp, url_prefix='/api')
    
    from . import webscrape
    app.register_blueprint(webscrape.bp, url_prefix='/api')

    jwt.init_app(app)
    mail.init_app(app)
    
    return app