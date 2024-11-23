from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from settings.admin_config import AdminConfig
from controllers.activities_controller import ActivitiesController

api = Blueprint('activities', __name__)

@api.route('/activities', methods=['GET'])
@jwt_required()
def obtener_actividades():
    user_id = get_jwt_identity()
    if user_id == AdminConfig.ADMIN_ID:
      try:
          ranking = ActivitiesController.obtener_actividades()
          return jsonify(ranking), 200
      except Exception as e:
          return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Content prohibited"}), 403

@api.route('/activities', methods=['POST'])
@jwt_required()
def guardar_actividad():
    user_id = get_jwt_identity()
    data = request.get_json()
    exito = ActivitiesController.guardar_actividad(
        nombre_actividad= data.get('nombre_actividad', 0),
        id_usuario=user_id,
        puntaje=data.get('puntaje', 0),
        puntaje_maximo=data.get('puntaje_maximo', 0),
    )
    if exito:
        return jsonify({"message": "Actividad guardado exitosamente"}), 201
    else:
        return jsonify({"error": "No se pudo guardar la Actividad"}), 500