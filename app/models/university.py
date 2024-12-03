import psycopg2
from app.utils.db_connection import get_db_connection

def get_all_universities():
    """
    Obtiene todas las universidades registradas en la base de datos.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para seleccionar universidades
        query = "SELECT university_id, name FROM universities;"
        cursor.execute(query)
        universities = cursor.fetchall()

        cursor.close()
        return [{"university_id": row[0], "name": row[1]} for row in universities]

    except psycopg2.Error as e:
        raise Exception(f"Error al obtener universidades: {e}")

    finally:
        if connection:
            connection.close()
