import os

basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ["true", "yes", "on", "1"]
    return False


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    ALCHEMY_TRACK_MODIFICATIONS = False
    USE_CORS = as_bool(os.environ.get("USE_CORS") or "yes")
    CORS_SUPPORTS_CREDENTIALS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ALCHEMICAL_DATABASE_URL = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    # API documentation
    APIFAIRY_TITLE = "Calendar-Interview API"
    APIFAIRY_VERSION = "1.0"
    APIFAIRY_UI = os.environ.get("DOCS_UI", "elements")


class TestingConfig(Config):
    TESTING = True
    ALCHEMICAL_DATABASE_URL = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    PRODUCTION = True
    ALCHEMICAL_DATABASE_URL = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
