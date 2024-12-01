import psycopg2
from psycopg2.extras import RealDictCursor
from app.utils.db_connection import get_db_connection
import datetime

class ReviewModel:
    def __init__(self):
        self.connection = get_db_connection()

    def get_all_reviews(self):
        """
        Obtiene todas las reseñas.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM Review")
                return cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener las reseñas: {e}")

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
        
    def get_all_reviews_with_names(self):
        """
        Obtiene todas las reseñas con los nombres de las universidades, usuarios y campus.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        r.review_id,
                        r.review,
                        r.image_name,
                        r.create_date,
                        r.up_vote,
                        r.down_vote,
                        r.state,
                        u.name AS user_name,         -- Nombre del usuario
                        un.name AS university_name, -- Nombre de la universidad asociada a la reseña
                        c.name AS campus_name       -- Nombre del campus
                    FROM 
                        Review r
                    INNER JOIN 
                        users u ON r.user_id = u.user_id
                    INNER JOIN 
                        universities un ON r.university_id = un.university_id
                    LEFT JOIN 
                        campus c ON r.campus_id = c.id -- JOIN con la tabla de campus
                """)
                return cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener las reseñas con nombres: {e}")

    def get_reviews_by_user(self, user_id):
        """
        Obtiene todas las reseñas asociadas a un usuario específico.
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * 
                    FROM Review 
                    WHERE user_id = %s
                """, (user_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Error al obtener las reseñas del usuario: {e}")
    
    def create_review(self, review_data):
        query = """
        INSERT INTO Review (review, user_id, image_name, create_date, up_vote, down_vote, university_id, state, campus_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    review_data['state'],
                    review_data.get('campus_id', None)  # Aquí tomamos el campus_id, que puede ser nulo
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
                cursor.execute("DELETE FROM review WHERE review_id = %s", (review_id,))
                self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Error al eliminar la reseña: {e}")
        
    def update_votes(self, review_id, vote_type):
        """
        Actualiza los votos de una reseña.
        """
        if vote_type == 'up':
            query = "UPDATE review SET up_vote = up_vote + 1 WHERE review_id = %s"
        elif vote_type == 'down':
            query = "UPDATE review SET down_vote = down_vote + 1 WHERE review_id = %s"
        else:
            raise Exception("Tipo de voto inválido.")
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (review_id,))
                self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Error al actualizar los votos: {e}")

    def get_total_votes(self, review_id):
        """
        Calcula el total de votos netos (up_vote - down_vote).
        """
        query = """
        SELECT 
            up_vote - down_vote AS total_votes 
        FROM 
            review 
        WHERE 
            review_id = %s
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (review_id,))
                result = cursor.fetchone()
                return result['total_votes'] if result else None
        except psycopg2.Error as e:
            raise Exception(f"Error al calcular el total de votos: {e}")
