from flask import jsonify
from database.db import get_connection

def get_all_questions():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Consulta para obtener todas las preguntas
        query = "SELECT id, text, created_at FROM questions"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Transformar las filas obtenidas en una lista de diccionarios
        questions = []
        for row in rows:
            questions.append({
                "id": row[0],
                "text": row[1],
                "created_at": row[2]
            })

        cursor.close()
        connection.close()

        return jsonify({"success": True, "data": questions}), 200

    except Exception as ex:
        return jsonify({"success": False, "error": f"Error al obtener las preguntas: {str(ex)}"}), 500
