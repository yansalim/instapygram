"""
Entry point for the Pipegram Flask application.

This module loads environment variables via python‑dotenv, constructs the
Flask application using the factory pattern and runs it. When deployed
under Gunicorn the `CMD` defined in the Dockerfile will call this file
without using the built‑in Flask development server.
"""
from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    # For local development only. In production use gunicorn.
    app.run(host="0.0.0.0", port=5000, debug=True)