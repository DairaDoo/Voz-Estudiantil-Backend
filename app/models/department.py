import psycopg2
from app.utils.db_connection import get_db_connection

def create_department(department_id, name, university_id):
    """
    Crea un nuevo departamento en la base de datos.
    
    :param department_id: ID único del departamento.
    :param name: Nombre del departamento (máximo 50 caracteres).
    :param university_id: ID de la universidad asociada.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para insertar un nuevo departamento
        query = """
        INSERT INTO Department (department_id, name, university_id)
        VALUES (%s, %s, %s)
        RETURNING department_id;
        """
        cursor.execute(query, (department_id, name, university_id))
        connection.commit()

        # Obtén el ID del departamento recién insertado
        new_department_id = cursor.fetchone()[0]
        cursor.close()
        return {"message": "Departamento creado con éxito", "department_id": new_department_id}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        raise Exception(f"Error al crear el departamento: {e}")

    finally:
        if connection:
            connection.close()


def get_all_departments():
    """
    Obtiene todos los departamentos registrados en la base de datos.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para seleccionar todos los departamentos
        query = """
        SELECT department_id, name, university_id 
        FROM Department;
        """
        cursor.execute(query)
        departments = cursor.fetchall()

        cursor.close()
        return [
            {"department_id": row[0], "name": row[1], "university_id": row[2]} 
            for row in departments
        ]

    except psycopg2.Error as e:
        raise Exception(f"Error al obtener los departamentos: {e}")

    finally:
        if connection:
            connection.close()


def get_department_by_id(department_id):
    """
    Obtiene un departamento por su ID.
    
    :param department_id: ID del departamento a buscar.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para seleccionar un departamento por ID
        query = """
        SELECT department_id, name, university_id 
        FROM Department
        WHERE department_id = %s;
        """
        cursor.execute(query, (department_id,))
        department = cursor.fetchone()

        cursor.close()

        if department:
            return {"department_id": department[0], "name": department[1], "university_id": department[2]}
        else:
            return {"message": "Departamento no encontrado"}

    except psycopg2.Error as e:
        raise Exception(f"Error al obtener el departamento: {e}")

    finally:
        if connection:
            connection.close()


def update_department(department_id, name=None, university_id=None):
    """
    Actualiza un departamento en la base de datos.
    
    :param department_id: ID único del departamento a actualizar.
    :param name: Nuevo nombre del departamento (opcional).
    :param university_id: Nueva universidad asociada (opcional).
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query dinámica para actualizar un departamento
        query = "UPDATE Department SET "
        updates = []
        params = []

        if name:
            updates.append("name = %s")
            params.append(name)
        if university_id:
            updates.append("university_id = %s")
            params.append(university_id)

        query += ", ".join(updates)
        query += " WHERE department_id = %s RETURNING department_id;"
        params.append(department_id)

        cursor.execute(query, tuple(params))
        connection.commit()

        updated_department_id = cursor.fetchone()
        cursor.close()

        if updated_department_id:
            return {"message": "Departamento actualizado con éxito", "department_id": updated_department_id[0]}
        else:
            return {"message": "Departamento no encontrado"}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        raise Exception(f"Error al actualizar el departamento: {e}")

    finally:
        if connection:
            connection.close()


def delete_department(department_id):
    """
    Elimina un departamento por su ID.
    
    :param department_id: ID del departamento a eliminar.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query para eliminar un departamento
        query = """
        DELETE FROM Department
        WHERE department_id = %s
        RETURNING department_id;
        """
        cursor.execute(query, (department_id,))
        connection.commit()

        deleted_department_id = cursor.fetchone()
        cursor.close()

        if deleted_department_id:
            return {"message": "Departamento eliminado con éxito", "department_id": deleted_department_id[0]}
        else:
            return {"message": "Departamento no encontrado"}

    except psycopg2.Error as e:
        if connection:
            connection.rollback()
        raise Exception(f"Error al eliminar el departamento: {e}")

    finally:
        if connection:
            connection.close()
