import psycopg2
import datetime
from app.utils.db_connection import get_db_connection  # Asumiendo que tienes esta función para obtener la conexión

class EventModel:
    def __init__(self):
        self.conn = get_db_connection()  # Conexión a la base de datos

    def create_event(self, event_data):
        """
        Crea un nuevo evento en la base de datos.
        """
        query = """
        INSERT INTO event (event_title, description, user_id, university_id, image_name, create_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING event_id;
        """
        try:
            with self.conn.cursor() as cursor:
                create_date = datetime.datetime.utcnow()  # Fecha y hora actuales en formato UTC
                cursor.execute(query, (
                    event_data['title'], 
                    event_data['description'], 
                    event_data['user_id'], 
                    event_data['university_id'], 
                    event_data.get('image_name', None),  # Si no hay imagen, pasa None
                    create_date
                ))
                event_id = cursor.fetchone()[0]
                self.conn.commit()
                return {"message": "Evento creado con éxito", "event_id": event_id}
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear el evento: {e}")

    def get_event(self, event_id):
        """
        Obtiene un evento por su ID.
        """
        query = """
        SELECT event_id, event_title, description, user_id, university_id, create_date, image_name
        FROM event
        WHERE event_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (event_id,))
                event = cursor.fetchone()

            if event:
                return {
                    "event_id": event[0],
                    "event_title": event[1],
                    "description": event[2],
                    "user_id": event[3],
                    "university_id": event[4],
                    "create_date": event[5],
                    "image_name": event[6]
                }
            else:
                return {"message": "Evento no encontrado"}
        except Exception as e:
            raise Exception(f"Error al obtener el evento: {e}")

    def get_all_events(self):
        """
        Obtiene todos los eventos registrados en la base de datos.
        """
        query = """
        SELECT event_id, event_title, description, user_id, university_id, create_date, image_name
        FROM event;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                events = cursor.fetchall()

            return [
                {
                    "event_id": row[0],
                    "event_title": row[1],
                    "description": row[2],
                    "user_id": row[3],
                    "university_id": row[4],
                    "create_date": row[5],
                    "image_name": row[6]
                }
                for row in events
            ]
        except Exception as e:
            raise Exception(f"Error al obtener todos los eventos: {e}")
