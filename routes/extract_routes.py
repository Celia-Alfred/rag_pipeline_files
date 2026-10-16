from flask import Blueprint, jsonify
from services.mysql_service import get_db_connection


extract_bp = Blueprint("extract", __name__)


@extract_bp.route("/api/extract", methods=["GET"])
def extract_data():

    connection = None
    cursor = None

    try:
        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, content, category, created_at
            FROM document
        """)

        records = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(records),
            "data": records
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()