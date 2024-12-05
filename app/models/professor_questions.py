import psycopg2
from app.utils.db_connection import get_db_connection

class ProfessorQuestion:
    def __init__(self):
        self.conn = get_db_connection()

    def get_all_questions(self):
        query = """
        SELECT question_id, question_text
        FROM professors_questions;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            questions = [{"question_id": row[0], "question_text": row[1]} for row in results]
            return questions
        except Exception as e:
            raise Exception(f"Error al obtener las preguntas: {e}")
        
    def get_question_by_id(self, question_id):
        query = """
        SELECT question_id, question_text
        FROM professors_questions WHERE question_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (question_id,))  # Pasa el parámetro correctamente
                result = cursor.fetchone()  # Solo un resultado esperado

            if result:
                return {"question_id": result[0], "question_text": result[1]}
            else:
                return None  # Si no encuentra la pregunta

        except Exception as e:
            raise Exception(f"Error al obtener la pregunta: {e}")
