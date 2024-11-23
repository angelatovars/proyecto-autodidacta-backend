from models.ranking_model import RankingModel

class RankingController:

    @staticmethod
    def guardar_puntaje(user_id, puntaje_total):
        try:
            # Llamar al modelo para guardar el puntaje en la base de datos
            return RankingModel.guardar_puntaje(user_id, puntaje_total)
        except Exception as e:
            print(f"Error al guardar puntaje: {str(e)}")
            return False

    @staticmethod
    def obtener_ranking():
        try:
            # Llamar al modelo para obtener el ranking desde la base de datos
            ranking = RankingModel.obtener_ranking()
            return ranking
        except Exception as e:
            print(f"Error al obtener ranking: {str(e)}")
            return []
    