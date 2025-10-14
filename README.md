# BBA Portfolio

A Flask + SQLite application that powers a portfolio gallery with an admin console. The backend exposes JSON APIs for managing portfolio items and users, while the frontend (vanilla HTML/CSS/JS) renders the site and provides admin workflows.

## Features
- Flask application factory (`src/main.py`) with configurable environment-driven settings.
- SQLite-backed SQLAlchemy models for `User` and `PortfolioItem` records.
- REST-style routes for listing, creating, updating, and deleting users.
- Portfolio routes with admin authentication for adding or removing gallery items.
- Static frontend in `src/static` that consumes the API, including an admin dashboard and media modal.
- CLI helper (`flask --app src.main seed-portfolio`) that seeds sample data.

## Requirements
- Python 3.11+
- pip
- (Optional) virtual environment tool such as `venv`

## Quick Start
1. **Clone & enter the project directory**
   ```bash
   git clone <repo-url>
   cd Mywebsite
   ```

2. **Create & activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   .\\venv\\Scripts\\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env` in the repository root.
   - Update values (especially `SECRET_KEY` and `ADMIN_SECRET_ID`) to suit your environment.

5. **Initialize the database**
   - The app will create `src/database/app.db` on first run.
   - To seed sample portfolio entries:
     ```bash
     flask --app src.main seed-portfolio
     ```

6. **Run the development server**
   ```bash
   flask --app src.main run
   ```
   Visit http://127.0.0.1:5000 to view the portfolio. The admin panel is served at `/admin.html`.

## API Overview
Base URL: `/api`

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/portfolio` | List all portfolio items (public). |
| POST | `/portfolio` | Add one or more portfolio items (admin only; expects `admin_id` and `items`). |
| DELETE | `/portfolio/<item_id>` | Remove a portfolio item (admin only). |
| POST | `/admin/login` | Validate admin ID. |
| GET | `/users` | List all users. |
| POST | `/users` | Create a user (`username`, `email`). |
| GET | `/users/<user_id>` | Retrieve a single user. |
| PUT | `/users/<user_id>` | Update a user (partial updates supported). |
| DELETE | `/users/<user_id>` | Delete a user. |

### Authentication
- Portfolio mutations require sending the `admin_id` field that matches `ADMIN_SECRET_ID`.
- The frontend admin panel handles this exchange once the admin logs in.

### Validation & Errors
- JSON bodies are required for write operations.
- The API returns structured error messages with appropriate HTTP status codes (400, 401, 404, 409, 500).

## Frontend Notes
- `src/static/index.html` renders the public gallery and consumes `/api/portfolio`.
- Media items open inside a modal with image/video support.
- `src/static/admin.html` implements login, item creation, and deletion workflows.

## Database Seeding
The production app no longer seeds data automatically. Use the provided CLI command; it inserts a trimmed set of sample records. You can customize `src/database/seed.py` or add your own scripts.

## Development Tips
- Run `flask --app src.main shell` to open an interactive context with `db`, `User`, and `PortfolioItem` imported.
- Adjust the `DATABASE_URL` in `.env` to point at a different database (PostgreSQL, MySQL, etc.) while keeping SQLAlchemy syntax-compatible.
- Enable debug mode by setting `FLASK_DEBUG=1` in your `.env`.

## License
Provide your preferred license here (currently unspecified).
