from http import HTTPStatus

from alchemical.flask import Alchemical
from apifairy import APIFairy
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from config import Config
from config import config

db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
api = APIFairy()


def create_app(config_name=Config):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from application import models

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    if app.config["USE_CORS"]:
        cors.init_app(app)
    api.init_app(app)

    """Blueprint"""
    from application.status.routes import status_bp as status
    from application.candidate.routes import candidate
    from application.interviewer.routes import interviewer
    from application.calendar.routers import calendar

    app.register_blueprint(status, url_prefix="/api")
    app.register_blueprint(candidate, url_prefix="/api")
    app.register_blueprint(interviewer, url_prefix="/api")
    app.register_blueprint(calendar, url_prefix="/api")

    return app


def page_not_found(error):
    return "<h1>Page not found.</h1>", HTTPStatus.NOT_FOUND
