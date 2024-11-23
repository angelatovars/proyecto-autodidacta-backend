from models.games_model import GamesModel


class GamesController:
    @staticmethod
    def guardar_game(nombre_juego,id_usuario,puntaje,puntaje_maximo):
        try:

            resultado = GamesModel.guardar_juego(
                nombre_juego, id_usuario, puntaje, puntaje_maximo
            )

            if resultado:
                return {"success": True, "message": "Juego guardado exitosamente."}
            else:
                return {"success": False, "message": "No se pudo guardar el juego."}
        except Exception as e:
            print(f"Error en guardar_game: {str(e)}")
            return {"success": False, "message": f"Error interno: {str(e)}"}

    @staticmethod
    def obtener_games():
        try:
            # Llamar al modelo para obtener el ranking desde la base de datos
            ranking = GamesModel.obtener_games()
            return ranking
        except Exception as e:
            print(f"Error al obtener juegos: {str(e)}")
            return []
