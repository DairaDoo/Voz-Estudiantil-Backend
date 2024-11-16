import psycopg2

# URL de conexión a la base de datos
DATABASE_URL = 'postgresql://postgres.auqgonswvvsvdakrwsga:voz_estudiantil_password@aws-0-us-west-1.pooler.supabase.com:6543/postgres'

def get_db_connection():
    """
    Obtiene una conexión a la base de datos.
    """
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        raise
