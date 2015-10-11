from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.compress import Compress
from config import config

db = MongoAlchemy()
compress = Compress()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    GoogleMaps(app)
    compress.init_app(app)

    # attach routes and custom error pages here

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app