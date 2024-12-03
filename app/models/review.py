import psycopg2
from psycopg2.extras import RealDictCursor
from app.utils.db_connection import get_db_connection
import datetime

class ReviewModel:
    def __init__(self):
        self.connection = get_db_connection()

    def get_review(self, review_id):
        """
        Obtiene una reseña por su ID.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM Review WHERE review_id = %s", (review_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener la reseña: {e}")

    def create_review(self, review_data):
        query = """
        INSERT INTO Review (review, user_id, image_name, create_date, up_vote, down_vote, university_id, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING review_id
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    review_data['review'],
                    review_data['user_id'],
                    review_data.get('image_name'),
                    review_data.get('create_date', datetime.datetime.utcnow()),
                    review_data.get('up_vote', 0),
                    review_data.get('down_vote', 0),
                    review_data['university_id'],
                    review_data['state']
                ))
                self.connection.commit()
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            raise Exception(f"Error al crear la reseña: {e}")


    def update_review(self, review_id, review_data):
        """
        Actualiza una reseña existente por su ID.
        """
        query = """
        UPDATE Review
        SET review = %s, image_name = %s, up_vote = %s, down_vote = %s, state = %s
        WHERE review_id = %s
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    review_data['review'],
                    review_data.get('image_name'),
                    review_data.get('up_vote', 0),
                    review_data.get('down_vote', 0),
                    review_data['state'],
                    review_id
                ))
                self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Error al actualizar la reseña: {e}")

    def delete_review(self, review_id):
        """
        Elimina una reseña por su ID.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM Review WHERE review_id = %s", (review_id,))
                self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Error al eliminar la reseña: {e}")
