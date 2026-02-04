import bcrypt
from flask import Blueprint, jsonify, request, session
from db import get_connection


auth_bp = Blueprint("auth", __name__)


def require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return user_id


@auth_bp.route("/session", methods=["GET"])
def session_info():
    user_id = session.get("user_id")
    username = session.get("username")
    if not user_id:
        return jsonify({"authenticated": False})
    return jsonify({"authenticated": True, "user_id": user_id, "username": username})


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    identifier = payload.get("identifier", "").strip()
    password = payload.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Credenziali mancanti"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, username, email, password_hash FROM users WHERE username=%s OR email=%s",
        (identifier, identifier),
    )
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({"error": "Credenziali non valide"}), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return jsonify({"message": "Login effettuato", "username": user["username"]})


@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Logout effettuato"})
