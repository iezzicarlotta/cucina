from flask import Blueprint, jsonify, request
from auth import require_login
from db import get_connection
from ricette import _recipe_cost


carrello_bp = Blueprint("carrello", __name__)


def _get_or_create_cart(cursor, user_id):
    cursor.execute(
        "SELECT id FROM carts WHERE user_id=%s AND status='active'",
        (user_id,),
    )
    cart = cursor.fetchone()
    if cart:
        return cart["id"]
    cursor.execute(
        "INSERT INTO carts (user_id, status) VALUES (%s, 'active')",
        (user_id,),
    )
    return cursor.lastrowid


@carrello_bp.route("/carrello/add", methods=["POST"])
def add_to_cart():
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "Autenticazione richiesta"}), 401

    payload = request.get_json(silent=True) or {}
    recipe_id = payload.get("recipe_id")
    people = payload.get("people")
    wine_id = payload.get("wine_id")

    if not recipe_id or not people:
        return jsonify({"error": "Dati mancanti"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cart_id = _get_or_create_cart(cursor, user_id)

    recipe_cost = _recipe_cost(cursor, recipe_id)
    subtotal = recipe_cost * int(people)

    wine_price = 0
    if wine_id:
        cursor.execute("SELECT price FROM wines WHERE id=%s", (wine_id,))
        wine_row = cursor.fetchone()
        wine_price = float(wine_row["price"]) if wine_row else 0
    subtotal += wine_price

    cursor.execute(
        """
        INSERT INTO cart_items (cart_id, recipe_id, people, wine_id, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (cart_id, recipe_id, people, wine_id, subtotal),
    )
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Ricetta aggiunta al carrello"})


@carrello_bp.route("/carrello", methods=["GET"])
def get_cart():
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "Autenticazione richiesta"}), 401

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM carts WHERE user_id=%s AND status='active'",
        (user_id,),
    )
    cart = cursor.fetchone()
    if not cart:
        cursor.close()
        connection.close()
        return jsonify({"items": [], "total": 0})

    cursor.execute(
        """
        SELECT ci.id, ci.people, ci.subtotal, r.title, r.image_url,
               w.name AS wine_name
        FROM cart_items ci
        JOIN recipes r ON r.id = ci.recipe_id
        LEFT JOIN wines w ON w.id = ci.wine_id
        WHERE ci.cart_id = %s
        """,
        (cart["id"],),
    )
    items = cursor.fetchall()
    total = sum(float(item["subtotal"]) for item in items)

    cursor.close()
    connection.close()

    return jsonify({"items": items, "total": total})


@carrello_bp.route("/carrello/remove", methods=["DELETE"])
def remove_from_cart():
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "Autenticazione richiesta"}), 401

    payload = request.get_json(silent=True) or {}
    item_id = payload.get("item_id")
    if not item_id:
        return jsonify({"error": "ID mancante"}), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        DELETE ci FROM cart_items ci
        JOIN carts c ON c.id = ci.cart_id
        WHERE ci.id=%s AND c.user_id=%s AND c.status='active'
        """,
        (item_id, user_id),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Elemento rimosso"})
