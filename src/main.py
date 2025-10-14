import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from src.config import Config
from src.models.user import db
from src.routes.user import user_bp
from src.routes.portfolio import portfolio_bp

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


def create_app(config_class=None):
    app = Flask(__name__, static_folder=STATIC_DIR)
    app.config.from_object(config_class or Config)

    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        os.makedirs(upload_folder, exist_ok=True)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(portfolio_bp, url_prefix="/api")

    register_cli_commands(app)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        static_folder_path = app.static_folder
        if not static_folder_path:
            return "Static folder not configured", 404

        requested_path = os.path.join(static_folder_path, path)
        if path and os.path.exists(requested_path):
            return send_from_directory(static_folder_path, path)

        index_path = os.path.join(static_folder_path, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, "index.html")

        return "index.html not found", 404

    with app.app_context():
        db.create_all()

    return app


def register_cli_commands(app):
    @app.cli.command("seed-portfolio")
    def seed_portfolio_command():
        """Seed the database with sample portfolio items."""
        from src.database.seed import seed_sample_portfolio

        seed_sample_portfolio()


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=application.config.get("DEBUG", False))

