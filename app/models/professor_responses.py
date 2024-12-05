import psycopg2
from app.utils.db_connection import get_db_connection

class ProfessorResponse:
    def __init__(self):
        self.conn = get_db_connection()

    def create_response(self, user_id, professor_id, question_id, answer, state="pendiente"):
        """
        Crea una nueva respuesta y actualiza el overall_rating del profesor.
        """
        query = """
        INSERT INTO professors_responses (user_id, professor_id, question_id, answer, state)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING responses_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (user_id, professor_id, question_id, answer, state))
                response_id = cursor.fetchone()[0]
                self.conn.commit()

                # Actualizar el overall_rating del profesor
                self.calculate_overall_rating(professor_id)

                return response_id
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear la respuesta: {e}")

    def get_response(self, response_id):
        query = """
        SELECT r.responses_id, r.user_id, r.professor_id, r.question_id, r.answer, r.state, r.response_date,
               p.name AS professor_name, u.email AS user_email, q.question_text
        FROM professors_responses r
        JOIN professors p ON r.professor_id = p.professors_id
        JOIN users u ON r.user_id = u.user_id
        JOIN professors_questions q ON r.question_id = q.question_id
        WHERE r.responses_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (response_id,))
                result = cursor.fetchone()
            if not result:
                return None
            return {
                "response_id": result[0],
                "user_id": result[1],
                "professor_id": result[2],
                "question_id": result[3],
                "answer": result[4],
                "state": result[5],
                "response_date": result[6],
                "professor_name": result[7],
                "user_email": result[8],
                "question_text": result[9],
            }
        except Exception as e:
            raise Exception(f"Error al obtener la respuesta: {e}")

    def update_response(self, response_id, answer=None, state=None):
        """
        Actualiza una respuesta y actualiza el overall_rating del profesor.
        """
        updates = []
        params = []
        if answer:
            updates.append("answer = %s")
            params.append(answer)
        if state:
            updates.append("state = %s")
            params.append(state)

        if not updates:
            raise ValueError("No hay campos para actualizar")

        query = f"UPDATE professors_responses SET {', '.join(updates)} WHERE response_id = %s RETURNING professor_id;"
        params.append(response_id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                professor_id = cursor.fetchone()[0]
                self.conn.commit()

                # Actualizar el overall_rating del profesor
                self.calculate_overall_rating(professor_id)

                return response_id
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al actualizar la respuesta: {e}")

    def delete_response(self, response_id):
        query = "DELETE FROM professors_responses WHERE responses_id = %s;"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (response_id,))
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al eliminar la respuesta: {e}")

    def get_all_responses(self):
        query = """
        SELECT r.responses_id, r.user_id, r.professor_id, r.question_id, r.answer, r.state, r.response_date,
               p.name AS professor_name, u.email AS user_email, q.question_text
        FROM professors_responses r
        JOIN professors p ON r.professor_id = p.professors_id
        JOIN users u ON r.user_id = u.user_id
        JOIN professors_questions q ON r.question_id = q.question_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            responses = []
            for row in results:
                responses.append({
                    "response_id": row[0],
                    "user_id": row[1],
                    "professor_id": row[2],
                    "question_id": row[3],
                    "answer": row[4],
                    "state": row[5],
                    "response_date": row[6],
                    "professor_name": row[7],
                    "user_email": row[8],
                    "question_text": row[9],
                })
            return responses
        except Exception as e:
            raise Exception(f"Error al obtener todas las respuestas: {e}")
        
    def calculate_overall_rating(self, professor_id):
        """
        Calcula el promedio de las respuestas de un profesor y actualiza el campo overall_rating.
        """
        query_average = """
        SELECT AVG(answer) AS average_rating
        FROM professors_responses
        WHERE professor_id = %s;
        """
        update_professor = """
        UPDATE professors
        SET overall_rating = %s
        WHERE professors_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                # Calcular el promedio
                cursor.execute(query_average, (professor_id,))
                average_rating = cursor.fetchone()[0]

                # Actualizar el rating del profesor
                if average_rating is not None:
                    cursor.execute(update_professor, (round(average_rating, 2), professor_id))
                    self.conn.commit()
                return round(average_rating, 2) if average_rating is not None else None
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al calcular y actualizar el promedio del profesor: {e}")
