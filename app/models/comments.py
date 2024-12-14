import psycopg2
from app.utils.db_connection import get_db_connection  # Asumiendo que tienes esta función para obtener la conexión

class CommentModel:
    def __init__(self):
        self.conn = get_db_connection()

    def create_comment(self, comment_data):
        """
        Crea un nuevo comentario en la base de datos.
        """
        query = """
        INSERT INTO Comment (review_id, comment, user_id)
        VALUES (%s, %s, %s)
        RETURNING comment_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (
                    comment_data['review_id'],
                    comment_data['comment'],
                    comment_data['user_id']
                ))
                comment_id = cursor.fetchone()[0]
                self.conn.commit()
                return comment_id
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear el comentario: {e}")

    def get_all_comments(self):
        """
        Obtiene todos los comentarios registrados en la base de datos.
        """
        query = """
        SELECT comment_id, review_id, comment, user_id
        FROM comment;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                comments = cursor.fetchall()
            return [
                {
                    "comment_id": row[0],
                    "review_id": row[1],
                    "comment": row[2],
                    "user_id": row[3],
                }
                for row in comments
            ]
        except Exception as e:
            raise Exception(f"Error al obtener los comentarios: {e}")

    def get_all_comments_with_usernames(self):
        """
        Obtiene todos los comentarios junto con el nombre del usuario que los realizó.
        """
        query = """
        SELECT 
            c.comment_id, 
            c.comment,
            u.name AS user_name
        FROM 
            comment c
        JOIN 
            users u ON c.user_id = u.user_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                comments = cursor.fetchall()
            return [
                {
                    "comment_id": row[0],
                    "comment": row[1],
                    "user_name": row[2]  # Aquí usamos el nombre del usuario
                }
                for row in comments
            ]
        except Exception as e:
            raise Exception(f"Error al obtener comentarios con nombres de usuario: {e}")

    def get_comments_by_review(self, review_id):
        """
        Obtiene los comentarios asociados a un 'review_id' específico.
        """
        query = """
        SELECT 
            c.comment_id, 
            c.comment,
            u.name AS user_name
        FROM 
            comment c
        JOIN 
            users u ON c.user_id = u.user_id
        WHERE 
            c.review_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (review_id,))
                comments = cursor.fetchall()
            return [
                {
                    "comment_id": row[0],
                    "comment": row[1],
                    "user_name": row[2]
                }
                for row in comments
            ]
        except Exception as e:
            raise Exception(f"Error al obtener los comentarios del review {review_id}: {e}")
