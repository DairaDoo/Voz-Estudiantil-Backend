import psycopg2

# URL de conexión a la base de datos
DATABASE_URL = 'postgresql://voz_estudiantil_user:XJq1zZcmlaoGd4Tumb5JeGAqQrrXuGUc@db:5432/voz_estudiantil_db_hd1d'

def get_db_connection():
    """
    Obtiene una conexión a la base de datos.
    """
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        raise
