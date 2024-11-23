from utils.db_config import create_connection

class ActivitiesModel:

    @staticmethod
    def guardar_actividad(nombre_actividad, id_usuario, puntaje, puntaje_maximo):
        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO actividades (nombre_actividad, id_usuario, puntaje, puntaje_maximo)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (nombre_actividad, id_usuario, puntaje, puntaje_maximo))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al guardar la Actividad: {e}")
            return False
        finally:
            connection.close()


    @staticmethod
    def obtener_actividades():
        connection = create_connection()
        cursor = connection.cursor()
        query = """
        SELECT *
        FROM actividades
        """
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        
        return result

