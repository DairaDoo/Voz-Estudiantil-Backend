import psycopg2
from psycopg2 import sql
from app.utils.db_connection import get_db_connection
import bcrypt

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


# Función para obtener un usuario por su correo electrónico
def get_user_by_email(email):
    """Busca la data del usuario utilizando el email."""
    try:
        connection = get_db_connection()  # Reemplaza con tu conexión a la base de datos
        cursor = connection.cursor()

        query = sql.SQL("SELECT user_id, email, password, name FROM users WHERE email = %s")
        cursor.execute(query, (email,))
        
        user = cursor.fetchone()  # Esto devuelve una fila con los datos del usuario
        cursor.close()
        connection.close()

        if user:
            # Imprimir para depurar
            print(f"Tipo de dato de la contraseña: {type(user[2])}")
            print(f"Contraseña almacenada: {user[2]}")

            return {
                "user_id": user[0],
                "email": user[1],
                "password": user[2],  # Aquí debe ser un string
                "name": user[3]
            }
        return None  # Si no hay usuario, devolver None
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        return None

    
def verify_user_password(email, password):
    """Verifica que el password sea el mismo que el de la base de datos."""
    user = get_user_by_email(email)
    
    if user:
        db_password = user['password']
        
        # Verifica que la contraseña almacenada es un string
        if isinstance(db_password, str):
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                return user  # Si las credenciales son correctas, devolvemos el usuario
        else:
            raise ValueError("La contraseña recuperada de la base de datos no es válida.")
    
    return None  # Si no son correctas, devolvemos None



