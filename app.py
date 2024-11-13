from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configura la conexión a la base de datos PostgreSQL
DATABASE_URL = 'postgresql://postgres.auqgonswvvsvdakrwsga:voz_estudiantil_password@aws-0-us-west-1.pooler.supabase.com:6543/postgres'


def get_db_connection():
    """Conecta con la base de datos y devuelve la conexión."""
    print("Conectando a la base de datos...")
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return "¡Bienvenido a Voz Estudiantil!"

@app.route('/create_user', methods=['POST'])
def create_user():
    print("Recibiendo solicitud para crear usuario...")
    data = request.get_json()

    # Verifica los datos necesarios
    if not data or 'email' not in data or 'name' not in data or 'password' not in data:
        print("Datos incompletos:", data)
        return jsonify({"error": "Faltan datos necesarios para crear el usuario"}), 400

    # Verifica el formato del correo electrónico
    if '@' not in data['email']:
        print(f"Correo inválido: {data['email']}")
        return jsonify({"error": "Correo electrónico inválido"}), 400

    if len(data['password']) < 6:
        print(f"Contraseña demasiado corta: {data['password']}")
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

    # Asigna valores por defecto si los campos son nulos
    university_id = data.get('university_id', None)  # Puede ser None
    rol = data.get('rol', 'usuario')  # Default a 'usuario' si no se pasa

    print(f"Creando usuario con: {data['email']}, {data['name']}, {university_id}, {rol}")

    connection = None

    try:
        print("Conectando a la base de datos...")
        connection = get_db_connection()
        cursor = connection.cursor()

        # Inserción con los valores recibidos
        query = """
        INSERT INTO users (email, name, password, university_id, rol, create_date)
        VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING user_id;
        """
        values = (
            data['email'],
            data['name'],
            data['password'],
            university_id,
            rol
        )

        cursor.execute(query, values)

        # Obtiene el ID del nuevo usuario
        new_user_id = cursor.fetchone()[0]
        print(f"Usuario creado con ID: {new_user_id}")
        connection.commit()

        cursor.close()

        return jsonify({"message": "Usuario creado con éxito", "user_id": new_user_id}), 201

    except psycopg2.Error as e:
        # Si ocurre un error, lo logueamos
        print("Error en la base de datos:", e)
        return jsonify({"error": "Error al crear el usuario", "details": str(e)}), 500

    finally:
        if connection:
            print("Cerrando la conexión a la base de datos...")
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
