from flask import Blueprint, jsonify, request
from db import get_connection


ricette_bp = Blueprint("ricette", __name__)


def _recipe_cost(cursor, recipe_id):
    cursor.execute(
        """
        SELECT SUM(ri.quantita_per_persona * i.prezzo_per_unita) AS costo
        FROM RICETTA_INGREDIENTE ri
        JOIN INGREDIENTI i ON i.ID = ri.ID_INGREDIENTE
        WHERE ri.ID_RICETTA = %s
        """,
        (recipe_id,),
    )
    row = cursor.fetchone()
    return float(row["costo"] or 0)


@ricette_bp.route("/ricette", methods=["GET"])
def list_recipes():
    genre = request.args.get("genere")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if genre:
        cursor.execute(
            """
            SELECT r.ID as id, r.titolo as title, r.descrizione as description,
                   (SELECT m.url FROM MEDIA m WHERE m.ID_RICETTA = r.ID LIMIT 1) AS image_url
            FROM RICETTE r
            JOIN GENERE_RICETTA gr ON gr.ID_RICETTA = r.ID
            JOIN GENERI g ON g.ID = gr.ID_GENERE
            WHERE g.nome = %s
            """,
            (genre,),
        )
    else:
        cursor.execute(
            """
            SELECT r.ID as id, r.titolo as title, r.descrizione as description,
                   (SELECT m.url FROM MEDIA m WHERE m.ID_RICETTA = r.ID LIMIT 1) AS image_url
            FROM RICETTE r
            """
        )

    recipes = cursor.fetchall()
    for recipe in recipes:
        recipe["costo_per_persona"] = _recipe_cost(cursor, recipe["id"])

    cursor.close()
    connection.close()

    return jsonify(recipes)


@ricette_bp.route("/ricette/<int:recipe_id>", methods=["GET"])
def recipe_detail(recipe_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT ID as id, titolo as title, descrizione as description FROM RICETTE WHERE ID=%s",
        (recipe_id,),
    )
    recipe = cursor.fetchone()
    if not recipe:
        cursor.close()
        connection.close()
        return jsonify({"error": "Ricetta non trovata"}), 404

    # ingredienti
    cursor.execute(
        """
        SELECT i.nome AS name, i.unita_base AS unit, i.prezzo_per_unita AS price_per_unit,
               ri.quantita_per_persona AS qty_per_persona, ri.unita_misura
        FROM RICETTA_INGREDIENTE ri
        JOIN INGREDIENTI i ON i.ID = ri.ID_INGREDIENTE
        WHERE ri.ID_RICETTA = %s
        """,
        (recipe_id,),
    )
    recipe["ingredienti"] = cursor.fetchall()

    # vini consigliati
    cursor.execute(
        """
        SELECT v.ID AS id, v.nome AS name, v.tipo AS type, rv.annata
        FROM RICETTA_VINO rv
        JOIN VINI v ON v.ID = rv.ID_VINO
        WHERE rv.ID_RICETTA = %s
        """,
        (recipe_id,),
    )
    recipe["vini_consigliati"] = cursor.fetchall()
    recipe["image_url"] = None
    cursor.execute("SELECT url FROM MEDIA WHERE ID_RICETTA=%s LIMIT 1", (recipe_id,))
    img = cursor.fetchone()
    if img:
        recipe["image_url"] = img["url"]

    recipe["costo_per_persona"] = _recipe_cost(cursor, recipe_id)

    cursor.close()
    connection.close()

    return jsonify(recipe)
