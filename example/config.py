import os


class Baseconfig(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "My super secret key"

    # JWT settings
    GOOGLE_CLIENT_ID = None
    GOOGLE_CLIENT_SECRET = None
    GOOGLE_REDIRECT_URI = None
    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"


class ProductionConfig(Baseconfig):
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


class LocalConfig(Baseconfig):
    DEBUG = True


class TestConfig(Baseconfig):
    TESTING = True
