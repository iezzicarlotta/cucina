from flask import Blueprint, jsonify
from auth import require_login
from db import get_connection


ordini_bp = Blueprint("ordini", __name__)


@ordini_bp.route("/checkout", methods=["POST"])
def checkout():
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
        return jsonify({"error": "Carrello vuoto"}), 400

    cursor.execute(
        """
        SELECT recipe_id, people, wine_id, subtotal
        FROM cart_items
        WHERE cart_id=%s
        """,
        (cart["id"],),
    )
    items = cursor.fetchall()
    if not items:
        cursor.close()
        connection.close()
        return jsonify({"error": "Carrello vuoto"}), 400

    total = sum(float(item["subtotal"]) for item in items)
    cursor.execute(
        "INSERT INTO orders (user_id, total, status) VALUES (%s, %s, 'pagato')",
        (user_id, total),
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, recipe_id, people, wine_id, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, item["recipe_id"], item["people"], item["wine_id"], item["subtotal"]),
        )

    cursor.execute("UPDATE carts SET status='closed' WHERE id=%s", (cart["id"],))
    cursor.execute("DELETE FROM cart_items WHERE cart_id=%s", (cart["id"],))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Ordine completato", "order_id": order_id, "total": total})
