import os

basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "2a5f06ca788e46809e44bf1a0cd50ace"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
    # BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    # BOOTSTRAP_BOOTSWATCH_THEME = 'materia'
    # BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
    # BOOTSTRAP_BOOTSWATCH_THEME = 'yeti'


    assert MAIL_USERNAME and MAIL_USERNAME

    MAIL_SUBJECT_PREFIX = "[ heej ]"
    MAIL_SENDER = "HEEJ Admin <sisesu92@gmail.com>"
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")

    POSTS_PER_PAGE = 5

    ADMINS = os.environ.get("ADMINS", None)
    ADMINS = [x.strip() for x in ADMINS.split(",")]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "data-dev.sqlite"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}