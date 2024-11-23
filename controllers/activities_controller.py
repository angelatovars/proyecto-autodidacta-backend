from models.activity_model import ActivitiesModel


class ActivitiesController:
    @staticmethod
    def guardar_actividad(nombre_actividad,id_usuario,puntaje,puntaje_maximo):
        try:

            resultado = ActivitiesModel.guardar_actividad(
                nombre_actividad, id_usuario, puntaje, puntaje_maximo
            )

            if resultado:
                return {"success": True, "message": "Actividad guardado exitosamente."}
            else:
                return {"success": False, "message": "No se pudo guardar la Actividad."}
        except Exception as e:
            print(f"Error en guardar_game: {str(e)}")
            return {"success": False, "message": f"Error interno: {str(e)}"}

    @staticmethod
    def obtener_actividades():
        try:
            # Llamar al modelo para obtener el ranking desde la base de datos
            ranking = ActivitiesModel.obtener_actividades()
            return ranking
        except Exception as e:
            print(f"Error al obtener Actividades: {str(e)}")
            return []
