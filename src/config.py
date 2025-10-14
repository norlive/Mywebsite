import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLITE_PATH = os.path.join(BASE_DIR, "database", "app.db")


class Config:
    """Base configuration loaded into the Flask app."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SECRET_ID = os.environ.get("ADMIN_SECRET_ID", "BBA-ADMIN-LOGIN")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") in {"1", "true", "True"}
