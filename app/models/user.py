import psycopg2
from psycopg2 import sql
from app.utils.db_connection import get_db_connection

# Función para crear un usuario
def create_user(data):
    """
    Crea un usuario en la base de datos.
    """
    if not data or 'email' not in data or 'name' not in data or 'password' not in data:
        raise ValueError("Faltan datos necesarios para crear el usuario")

    # Validaciones específicas
    if '@' not in data['email']:
        raise ValueError("Correo electrónico inválido")

    if len(data['password']) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres")

    # Valores opcionales
    university_id = data.get('university_id', None)
    rol = data.get('rol', 'usuario')

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para insertar el usuario
        query = """
        INSERT INTO users (email, name, password, university_id, rol, create_date)
        VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING user_id;
        """
        values = (
            data['email'],
            data['name'],
            data['password'],
            university_id,
            rol,
        )

        cursor.execute(query, values)
        new_user_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()

        return {"message": "Usuario creado con éxito", "user_id": new_user_id}

    except psycopg2.Error as e:
        raise Exception(f"Error al crear el usuario: {e}")

    finally:
        if connection:
            connection.close()


def update_user_data(data):
    pass