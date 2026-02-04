from flask import Flask
from auth import auth_bp
from ricette import ricette_bp
from carrello import carrello_bp
from ordini import ordini_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(ricette_bp)
    app.register_blueprint(carrello_bp)
    app.register_blueprint(ordini_bp)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
