import os
from flask import Flask, jsonify, send_from_directory
from auth import auth_bp
from ricette import ricette_bp
from carrello import carrello_bp
from ordini import ordini_bp
from db import get_connection


def create_app():
    # Configure Flask to serve static files and templates from the frontend directory
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    app = Flask(__name__, static_folder=os.path.join(frontend_dir, 'css'), template_folder=frontend_dir)
    app.config["SECRET_KEY"] = "dev-secret-key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(ricette_bp)
    app.register_blueprint(carrello_bp)
    app.register_blueprint(ordini_bp)
    @app.route('/health', methods=['GET'])
    def health():
        try:
            conn = get_connection()
            # support both mysql.connector and sqlite wrapper
            cursor = conn.cursor(dictionary=True) if hasattr(conn, 'cursor') else conn.cursor()
            try:
                cursor.execute("SELECT 1")
            except Exception:
                # some SQLite cursors may need no params
                cursor.execute("SELECT 1")
            try:
                _ = cursor.fetchone()
            except Exception:
                pass
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'status': 'error', 'error': str(e)}), 500

    # serve frontend index at root if available
    @app.route('/', methods=['GET'])
    def index_root():
        try:
            # frontend is located one level up in repo under 'frontend'
            return send_from_directory(frontend_dir, 'index.html')
        except Exception:
            return "Homepage not available", 404

    return app  # Ensure the Flask app instance is returned


if __name__ == "__main__":
    app = create_app()  # Assign the Flask app instance to a variable
    app.run(host="0.0.0.0", port=5000, debug=False)
