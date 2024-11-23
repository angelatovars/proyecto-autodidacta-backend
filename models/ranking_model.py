from utils.db_config import create_connection

class RankingModel:

    @staticmethod
    def guardar_puntaje(user_id, puntaje_total):
        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO ranking (id_usuario, puntaje_total)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE puntaje_total = puntaje_total + VALUES(puntaje_total)
                """
                cursor.execute(query, (user_id, puntaje_total))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al guardar puntaje: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def obtener_ranking():
        connection = create_connection()  # Usamos tu método de conexión existente
        cursor = connection.cursor()

        # Consulta SQL con JOIN para obtener el nombre del usuario y el puntaje
        query = """
        SELECT usuarios.nombre, ranking.puntaje_total
        FROM ranking
        JOIN usuarios ON ranking.id_usuario = usuarios.id_usuario
        ORDER BY ranking.puntaje_total DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        
        return result

