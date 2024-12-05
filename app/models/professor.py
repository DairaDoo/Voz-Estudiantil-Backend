import psycopg2
from app.utils.db_connection import get_db_connection

class Professor:
    def __init__(self):
        """
        Inicializa la clase Professor con una conexión a la base de datos.
        """
        self.conn = get_db_connection()

    def create_professor(self, name, department_id, overall_rating, state="pendiente"):
        """
        Crea un nuevo profesor en la base de datos.
        """
        query = """
        INSERT INTO professors (name, department_id, overall_rating, state)
        VALUES (%s, %s, %s, %s)
        RETURNING professors_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (name, department_id, overall_rating, state))
                professor_id = cursor.fetchone()[0]
            self.conn.commit()
            return professor_id
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al crear el profesor: {e}")

    def get_professor(self, professor_id):
        """
        Obtiene un profesor por su ID.
        """
        query = "SELECT * FROM professors WHERE professors_id = %s;"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (professor_id,))
                result = cursor.fetchone()
            return result
        except Exception as e:
            raise Exception(f"Error al obtener el profesor: {e}")

    def update_professor(self, professor_id, name=None, department_id=None, overall_rating=None, state=None):
        """
        Actualiza los detalles de un profesor.
        """
        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if department_id:
            updates.append("department_id = %s")
            params.append(department_id)
        if overall_rating:
            updates.append("overall_rating = %s")
            params.append(overall_rating)
        if state:
            updates.append("state = %s")
            params.append(state)

        if not updates:
            raise ValueError("No hay campos para actualizar")

        query = f"UPDATE professors SET {', '.join(updates)} WHERE professors_id = %s RETURNING *;"
        params.append(professor_id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                result = cursor.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al actualizar el profesor: {e}")

    def delete_professor(self, professor_id):
        """
        Elimina un profesor por su ID.
        """
        query = "DELETE FROM professors WHERE professors_id = %s;"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (professor_id,))
            self.conn.commit()
            return cursor.rowcount  # Número de filas eliminadas
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al eliminar el profesor: {e}")
        
    def get_all_professors(self):
        """
        Obtiene todos los profesores con el nombre del departamento.
        """
        query = """
        SELECT p.professors_id, p.name, p.department_id, p.overall_rating, p.state, d.name as department_name
        FROM professors p
        LEFT JOIN department d ON p.department_id = d.department_id;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            professors = []
            for row in results:
                professors.append({
                    "professor_id": row[0],
                    "name": row[1],
                    "department_id": row[2],
                    "overall_rating": row[3],
                    "state": row[4],
                    "department_name": row[5]  # Aquí agregamos el nombre del departamento
                })
            return professors
        except Exception as e:
            raise Exception(f"Error al obtener todos los profesores: {e}")
