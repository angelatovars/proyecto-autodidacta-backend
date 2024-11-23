from utils.db_config import create_connection

class GamesModel:

    @staticmethod
    def guardar_juego(nombre_juego, id_usuario, puntaje, puntaje_maximo):
        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO juegos (nombre_juego, id_usuario, puntaje, puntaje_maximo)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (nombre_juego, id_usuario, puntaje, puntaje_maximo))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al guardar el juego: {e}")
            return False
        finally:
            connection.close()


    @staticmethod
    def obtener_games():
        connection = create_connection()  # Usamos tu método de conexión existente
        cursor = connection.cursor()

        # Consulta SQL con JOIN para obtener el nombre del usuario y el puntaje
        query = """
        SELECT *
        FROM juegos
        """
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        
        return result

