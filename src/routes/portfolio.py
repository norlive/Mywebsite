from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from src.models.user import db
from src.models.portfolio import PortfolioItem

portfolio_bp = Blueprint("portfolio", __name__)

VALID_MEDIA_TYPES = {"image", "video"}
REQUIRED_FIELDS = ("title", "src", "type", "category")


def _verify_admin(payload):
    admin_secret = current_app.config.get("ADMIN_SECRET_ID")
    provided = payload.get("admin_id") if payload else None
    return admin_secret and provided == admin_secret


def _normalize_item_payload(item_payload):
    normalized = {key: (item_payload.get(key) or "").strip() for key in REQUIRED_FIELDS}
    normalized["description"] = (item_payload.get("description") or "").strip()
    normalized["type"] = normalized["type"].lower()
    return normalized


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
