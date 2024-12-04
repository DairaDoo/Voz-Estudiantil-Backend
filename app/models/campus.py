import psycopg2
from app.utils.db_connection import get_db_connection

def get_campuses_by_university(university_id):
    """
    Obtiene los IDs y nombres de los campus asociados a una universidad específica.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para obtener los IDs y nombres de los campus
        query = """
        SELECT id, name
        FROM campus
        WHERE university_id = %s;
        """
        cursor.execute(query, (university_id,))
        campuses = cursor.fetchall()

        cursor.close()
        # Retornar una lista de diccionarios con campus_id y name
        return [{"id": row[0], "name": row[1]} for row in campuses]

    except psycopg2.Error as e:
        raise Exception(f"Error al obtener los campus: {e}")

    finally:
        if connection:
            connection.close()
