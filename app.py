import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# Load .env for local development only. In production (e.g. Azure) use real environment variables.
load_dotenv(override=False)

def create_app():
    app = Flask(__name__)

    # Configure CORS: allow any origin for the /products endpoint, only GET method
    # In production you may restrict origins via an env var.
    cors_origins = os.getenv("CORS_ORIGINS", "*")  # "*" by default
    CORS(app, resources={r"/products": {"origins": cors_origins}}, methods=["GET"])

    @app.route("/products", methods=["GET"])
    def products():
        # In a real app these would come from a backing DB - keep same static response as Rust version.
        items = [
            {"id": 1, "name": "Dog Food",  "price": 19.99},
            {"id": 2, "name": "Cat Food",  "price": 34.99},
            {"id": 3, "name": "Bird Seeds","price": 10.99},
        ]
        return jsonify(items)

    # Optional health endpoint used by platforms for liveness/readiness checks
    @app.route("/healthz", methods=["GET"])
    def health():
        return ("OK", 200)

    return app

# Create the application object for gunicorn to pick up as "app:app"
app = create_app()

if __name__ == "__main__":
    # Local dev run: pick PORT from env (Azure supplies PORT in production)
    port = int(os.getenv("PORT", "3030"))
    # debug mode should be controlled via env var; default False
    debug = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
