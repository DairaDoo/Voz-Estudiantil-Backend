import psycopg2

# URL de conexión a la base de datos
DATABASE_URL = 'postgresql://user:6VdM8xZjB08rT6vW2ClvQmBN0D1rWjfI@dpg-cthn8uqj1k6c739erpv0-a.oregon-postgres.render.com/voz_estudiantil_user'

def get_db_connection():
    """
    Obtiene una conexión a la base de datos.
    """
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        raise
