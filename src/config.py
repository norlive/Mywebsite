import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DEFAULT_SQLITE_PATH = os.path.join(BASE_DIR, "database", "app.db")

DEFAULT_UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
DEFAULT_MAX_UPLOAD_MB = 200


class Config:
    """Base configuration loaded into the Flask app."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SECRET_ID = os.environ.get("ADMIN_SECRET_ID", "BBA-ADMIN-LOGIN")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") in {"1", "true", "True"}
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_SIZE_MB", DEFAULT_MAX_UPLOAD_MB)) * 1024 * 1024
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", DEFAULT_UPLOAD_DIR)

    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
    ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm", "m4v"}
    ALLOWED_MEDIA_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

