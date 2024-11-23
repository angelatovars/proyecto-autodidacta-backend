from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from settings.admin_config import AdminConfig
from controllers.games_controller import GamesController

api = Blueprint('games', __name__)

@api.route('/games', methods=['GET'])
@jwt_required()
def obtener_juegos():
    user_id = get_jwt_identity()
    if user_id == AdminConfig.ADMIN_ID:
      try:
          ranking = GamesController.obtener_games()
          return jsonify(ranking), 200
      except Exception as e:
          return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Content prohibited"}), 403    
    

@api.route('/games', methods=['POST'])
@jwt_required()
def guardar_juego():
    data = request.get_json()
    user_id = get_jwt_identity()
    data = request.get_json()
    exito = GamesController.guardar_game(
        nombre_juego= data.get('nombre_juego', 0),
        id_usuario=user_id,
        puntaje=data.get('puntaje', 0),
        puntaje_maximo=data.get('puntaje_maximo', 0),
    )
    if exito:
        return jsonify({"message": "Juego guardado exitosamente"}), 201
    else:
        return jsonify({"error": "No se pudo guardar el juego"}), 500
