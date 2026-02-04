from flask import Blueprint, jsonify, request
from auth import require_login
from db import get_connection
from ricette import _recipe_cost


carrello_bp = Blueprint("carrello", __name__)


def _get_or_create_cart(cursor, user_id):
    cursor.execute(
        "SELECT ID FROM CARRELLI WHERE ID_UTENTE=%s",
        (user_id,),
    )
    cart = cursor.fetchone()
    if cart:
        return cart["ID"]
    cursor.execute(
        "INSERT INTO CARRELLI (ID_UTENTE) VALUES (%s)",
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
        cursor.execute("SELECT prezzo FROM VINI WHERE ID=%s", (wine_id,))
        wine_row = cursor.fetchone()
        wine_price = float(wine_row["prezzo"]) if wine_row and wine_row.get("prezzo") is not None else 0
    subtotal += wine_price

    cursor.execute(
        """
        INSERT INTO CARRELLO_ITEM (ID_CARRELLO, ID_RICETTA, persone, ID_VINO, prezzo_item)
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
        "SELECT ID FROM CARRELLI WHERE ID_UTENTE=%s",
        (user_id,),
    )
    cart = cursor.fetchone()
    if not cart:
        cursor.close()
        connection.close()
        return jsonify({"items": [], "total": 0})

    cursor.execute(
        """
        SELECT ci.ID as id, ci.persone as people, ci.prezzo_item as subtotal,
               r.titolo as title, (SELECT m.url FROM MEDIA m WHERE m.ID_RICETTA = r.ID LIMIT 1) as image_url,
               v.nome AS wine_name
        FROM CARRELLO_ITEM ci
        JOIN RICETTE r ON r.ID = ci.ID_RICETTA
        LEFT JOIN VINI v ON v.ID = ci.ID_VINO
        WHERE ci.ID_CARRELLO = %s
        """,
        (cart["ID"],),
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
        DELETE ci FROM CARRELLO_ITEM ci
        JOIN CARRELLI c ON c.ID = ci.ID_CARRELLO
        WHERE ci.ID=%s AND c.ID_UTENTE=%s
        """,
        (item_id, user_id),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Elemento rimosso"})
