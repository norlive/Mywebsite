from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.models.user import User, db

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route("/users", methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()

    if not username or not email:
        return jsonify({"error": "Both 'username' and 'email' are required."}), 400

    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists."}), 409
    except SQLAlchemyError as exc:
        db.session.rollback()
        user_bp.logger.exception("Failed to create user: %s", exc)
        return jsonify({"error": "Failed to create user."}), 500


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404
    return jsonify(user.to_dict())


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")

    if username is not None:
        username = username.strip()
        if not username:
            return jsonify({"error": "Username cannot be empty."}), 400
        user.username = username

    if email is not None:
        email = email.strip()
        if not email:
            return jsonify({"error": "Email cannot be empty."}), 400
        user.email = email

    try:
        db.session.commit()
        return jsonify(user.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists."}), 409
    except SQLAlchemyError as exc:
        db.session.rollback()
        user_bp.logger.exception("Failed to update user %s: %s", user_id, exc)
        return jsonify({"error": "Failed to update user."}), 500


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), 200
    except SQLAlchemyError as exc:
        db.session.rollback()
        user_bp.logger.exception("Failed to delete user %s: %s", user_id, exc)
        return jsonify({"error": "Failed to delete user."}), 500
