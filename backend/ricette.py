from flask import Blueprint, jsonify, request
from db import get_connection


ricette_bp = Blueprint("ricette", __name__)


def _recipe_cost(cursor, recipe_id):
    cursor.execute(
        """
        SELECT SUM(ri.qty_per_person * i.price_per_unit) AS costo
        FROM recipe_ingredients ri
        JOIN ingredients i ON i.id = ri.ingredient_id
        WHERE ri.recipe_id = %s
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
            "SELECT id, title, description, image_url, genre FROM recipes WHERE genre=%s",
            (genre,),
        )
    else:
        cursor.execute("SELECT id, title, description, image_url, genre FROM recipes")

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
        "SELECT id, title, description, image_url, genre FROM recipes WHERE id=%s",
        (recipe_id,),
    )
    recipe = cursor.fetchone()
    if not recipe:
        cursor.close()
        connection.close()
        return jsonify({"error": "Ricetta non trovata"}), 404

    cursor.execute(
        """
        SELECT i.name, i.unit, i.price_per_unit, ri.qty_per_person
        FROM recipe_ingredients ri
        JOIN ingredients i ON i.id = ri.ingredient_id
        WHERE ri.recipe_id = %s
        """,
        (recipe_id,),
    )
    recipe["ingredienti"] = cursor.fetchall()

    cursor.execute(
        """
        SELECT w.id, w.name, w.price
        FROM recipe_wines rw
        JOIN wines w ON w.id = rw.wine_id
        WHERE rw.recipe_id = %s
        """,
        (recipe_id,),
    )
    recipe["vini_consigliati"] = cursor.fetchall()
    recipe["costo_per_persona"] = _recipe_cost(cursor, recipe_id)

    cursor.close()
    connection.close()

    return jsonify(recipe)
