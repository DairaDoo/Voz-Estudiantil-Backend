import psycopg2
from app.utils.db_connection import get_db_connection

def create_rating(data):
    """
    Crea una calificación en la base de datos para un profesor.
    """
    if not data or 'professor_id' not in data or 'user_id' not in data or 'rating' not in data:
        raise ValueError("Faltan datos necesarios para crear la calificación")

    # Validaciones específicas
    rating = data['rating']
    if not (1 <= rating <= 5):
        raise ValueError("La calificación debe estar entre 1 y 5")

    # Convertir strings vacíos a None (NULL en PostgreSQL)
    professor_id = data['professor_id']
    user_id = data['user_id']
    comment = data.get('comment', None)

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para insertar la calificación
        query = """
        INSERT INTO ratings (professor_id, user_id, rating, comment, created_at)
        VALUES (%s, %s, %s, %s, NOW()) RETURNING rating_id;
        """
        values = (professor_id, user_id, rating, comment)

        cursor.execute(query, values)
        new_rating_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()

        return {"message": "Calificación creada con éxito", "rating_id": new_rating_id}

    except psycopg2.Error as e:
        raise Exception(f"Error al crear la calificación: {e}")

    finally:
        if connection:
            connection.close()


def get_ratings_by_professor(professor_id):
    """
    Obtiene todas las calificaciones de un profesor específico.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para seleccionar las calificaciones
        query = """
        SELECT rating_id, user_id, rating, comment, created_at
        FROM ratings
        WHERE professor_id = %s
        ORDER BY created_at DESC;
        """
        cursor.execute(query, (professor_id,))
        ratings = cursor.fetchall()

        cursor.close()
        return [
            {
                "rating_id": row[0],
                "user_id": row[1],
                "rating": row[2],
                "comment": row[3],
                "created_at": row[4]
            } for row in ratings
        ]

    except psycopg2.Error as e:
        raise Exception(f"Error al obtener calificaciones: {e}")

    finally:
        if connection:
            connection.close()
