from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from controllers.profile_controller import ProfileController

# Definir un Blueprint para las rutas del perfil
api = Blueprint('profile_api', __name__)
CORS(api)

# Ruta para obtener el perfil del usuario
@api.route('/api/profile', methods=['GET', 'PUT', 'OPTIONS'])
@cross_origin()
def profile():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
        
    correo = request.args.get('correo')  # Obtener el correo desde los parámetros de la URL
    
    if request.method == 'GET':
        return ProfileController.get_profile_by_email(correo)
    elif request.method == 'PUT':
        data = request.get_json()            # Obtener los datos del cuerpo de la solicitud
        return ProfileController.update_profile_by_email(correo, data)

