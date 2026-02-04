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
        "SELECT ID FROM CARRELLI WHERE ID_UTENTE=%s",
        (user_id,),
    )
    cart = cursor.fetchone()
    if not cart:
        cursor.close()
        connection.close()
        return jsonify({"error": "Carrello vuoto"}), 400

    cursor.execute(
        """
        SELECT ID_RICETTA as recipe_id, persone as people, ID_VINO as wine_id, prezzo_item as subtotal
        FROM CARRELLO_ITEM
        WHERE ID_CARRELLO=%s
        """,
        (cart["ID"],),
    )
    items = cursor.fetchall()
    if not items:
        cursor.close()
        connection.close()
        return jsonify({"error": "Carrello vuoto"}), 400

    total = sum(float(item["subtotal"]) for item in items)
    cursor.execute(
        "INSERT INTO ORDINI (ID_UTENTE, totale, stato) VALUES (%s, %s, 'pagato')",
        (user_id, total),
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            """
            INSERT INTO ORDINE_RICETTA (ID_ORDINE, ID_RICETTA, ID_VINO, persone, prezzo_item)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order_id, item["recipe_id"], item["wine_id"], item["people"], item["subtotal"]),
        )

    cursor.execute("UPDATE CARRELLI SET aggiornato=NOW() WHERE ID=%s", (cart["ID"],))
    cursor.execute("DELETE FROM CARRELLO_ITEM WHERE ID_CARRELLO=%s", (cart["ID"],))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Ordine completato", "order_id": order_id, "total": total})
