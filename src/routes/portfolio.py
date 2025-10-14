import os
from uuid import uuid4
from urllib.parse import urlparse

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from src.models.user import db
from src.models.portfolio import PortfolioItem

portfolio_bp = Blueprint("portfolio", __name__)

VALID_MEDIA_TYPES = {"image", "video"}
REQUIRED_FIELDS = ("title", "src", "type", "category")


def _verify_admin(payload):
    admin_secret = current_app.config.get("ADMIN_SECRET_ID")
    provided = payload.get("admin_id") if payload else None
    return admin_secret and provided == admin_secret


def _extract_extension_from_src(src_value):
    if not src_value:
        return ""

    parsed = urlparse(src_value)
    path = parsed.path or src_value
    _, extension = os.path.splitext(path)
    return extension.lstrip(".").lower()


def _infer_media_type_from_extension(extension):
    if not extension:
        return None

    image_exts = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", set())
    video_exts = current_app.config.get("ALLOWED_VIDEO_EXTENSIONS", set())

    if extension in image_exts:
        return "image"
    if extension in video_exts:
        return "video"
    return None


def _build_static_url(file_path):
    static_folder = current_app.static_folder
    if not static_folder:
        return None

    static_root = os.path.abspath(static_folder)
    absolute_path = os.path.abspath(file_path)

    try:
        common = os.path.commonpath([static_root, absolute_path])
    except ValueError:
        return None

    if common != static_root:
        return None

    relative_path = os.path.relpath(absolute_path, static_root)
    normalized = relative_path.replace(os.sep, "/")
    return f"/static/{normalized}"


def _save_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename or "")
    extension = filename.rsplit(".", 1)[1].lower() if "." in filename else ""

    media_type = _infer_media_type_from_extension(extension)
    if not media_type:
        raise ValueError("Unsupported file type. Please upload approved image or video formats.")

    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    if not upload_folder:
        raise ValueError("Upload folder is not configured.")

    os.makedirs(upload_folder, exist_ok=True)

    unique_name = f"{uuid4().hex}.{extension}" if extension else uuid4().hex
    saved_path = os.path.join(upload_folder, unique_name)

    file_storage.save(saved_path)

    public_src = _build_static_url(saved_path)
    if not public_src:
        os.remove(saved_path)
        raise ValueError("UPLOAD_FOLDER must be inside the static directory to serve files.")

    return {
        "src": public_src,
        "type": media_type,
        "filename": unique_name,
    }


def _normalize_item_payload(item_payload):
    normalized = {key: (item_payload.get(key) or "").strip() for key in REQUIRED_FIELDS}
    normalized["description"] = (item_payload.get("description") or "").strip()
    normalized["type"] = normalized["type"].lower()

    if normalized["type"] not in VALID_MEDIA_TYPES:
        inferred_type = _infer_media_type_from_extension(_extract_extension_from_src(normalized["src"]))
        if inferred_type:
            normalized["type"] = inferred_type

    return normalized


@portfolio_bp.route("/portfolio/upload", methods=["POST"])
def upload_portfolio_media():
    payload = request.form
    if not _verify_admin(payload):
        return jsonify({"error": "Unauthorized"}), 401

    file_storage = request.files.get("file")
    if file_storage is None or not file_storage.filename:
        return jsonify({"error": "No file provided."}), 400

    try:
        saved_info = _save_uploaded_file(file_storage)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except OSError as exc:  # pragma: no cover - filesystem edge cases
        current_app.logger.exception("Failed to store uploaded file: %s", exc)
        return jsonify({"error": "Failed to store uploaded file."}), 500

    return jsonify({"message": "Upload successful", **saved_info}), 201


@portfolio_bp.route("/portfolio", methods=["GET"])
def get_portfolio_items():
    try:
        items = PortfolioItem.query.order_by(PortfolioItem.created_at.desc()).all()
        return jsonify({"portfolio": [item.to_dict() for item in items]}), 200
    except SQLAlchemyError as exc:
        current_app.logger.exception("Failed to fetch portfolio items: %s", exc)
        return jsonify({"error": "Unable to fetch portfolio items."}), 500


@portfolio_bp.route("/portfolio", methods=["POST"])
def add_portfolio_item():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json() or {}

    if not _verify_admin(payload):
        return jsonify({"error": "Unauthorized"}), 401

    items_payload = payload.get("items")
    if not isinstance(items_payload, list) or not items_payload:
        return jsonify({"error": "'items' must be a non-empty list."}), 400

    created_items = []

    try:
        for index, item_payload in enumerate(items_payload, start=1):
            if not isinstance(item_payload, dict):
                db.session.rollback()
                return jsonify({"error": f"Item at position {index} is not valid JSON object."}), 400

            normalized = _normalize_item_payload(item_payload)
            missing = [field for field in REQUIRED_FIELDS if not normalized[field]]
            if missing:
                db.session.rollback()
                return jsonify({"error": f"Missing required fields for item {index}: {', '.join(missing)}."}), 400

            if normalized["type"] not in VALID_MEDIA_TYPES:
                db.session.rollback()
                return jsonify({"error": f"Invalid media type for item {index}."}), 400

            new_item = PortfolioItem(
                title=normalized["title"],
                src=normalized["src"],
                type=normalized["type"],
                category=normalized["category"],
                description=normalized["description"],
            )
            db.session.add(new_item)
            created_items.append(new_item)

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Items added successfully",
                    "items": [item.to_dict() for item in created_items],
                }
            ),
            201,
        )
    except SQLAlchemyError as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to add portfolio items: %s", exc)
        return jsonify({"error": "Failed to add portfolio items."}), 500


@portfolio_bp.route("/portfolio/<int:item_id>", methods=["DELETE"])
def delete_portfolio_item(item_id):
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json() or {}

    if not _verify_admin(payload):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        item = PortfolioItem.query.get(item_id)
        if item is None:
            return jsonify({"error": "Portfolio item not found."}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"}), 200
    except SQLAlchemyError as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to delete portfolio item %s: %s", item_id, exc)
        return jsonify({"error": "Failed to delete portfolio item."}), 500


@portfolio_bp.route("/admin/login", methods=["POST"])
def admin_login():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json() or {}
    try:
        if _verify_admin(payload):
            return jsonify({"success": True, "message": "Login successful"}), 200
        return jsonify({"success": False, "message": "Invalid Admin ID"}), 401
    except Exception as exc:  # pragma: no cover - defensive
        current_app.logger.exception("Admin login failed: %s", exc)
        return jsonify({"error": "Admin authentication failed."}), 500
