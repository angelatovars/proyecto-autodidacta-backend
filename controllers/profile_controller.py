from flask import jsonify
from models.user_model import UserModel
from models.profile_model import ProfileModel

class ProfileController:

    @staticmethod
    def get_profile_by_email(correo):
        user = UserModel.get_user_by_email(correo)  # Obtener usuario por correo
        
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        perfil = ProfileModel.get_profile_by_user_id(user["id_usuario"])  # Obtener perfil por ID de usuario

        if not perfil:
            return jsonify({"message": "Perfil no encontrado"}), 404

        # Devolver el perfil y datos del usuario
        return jsonify({
            "id_usuario": user["id_usuario"],
            "nombre": user["nombre"],
            "correo": user["correo"],
            "edad": user["edad"],
            "notificaciones": perfil["notificaciones"],
            "tema_preferido": perfil["tema_preferido"],
            "nivel_preferido": perfil["nivel_preferido"],
            "fecha_registro": user["fecha_registro"]
        }), 200

    @staticmethod
    def update_profile_by_email(correo, data):
        user = UserModel.get_user_by_email(correo)  # Obtener usuario por correo
        
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        success = ProfileModel.update_profile(user["id_usuario"], data)  # Actualizar el perfil por ID de usuario

        if not success:
            return jsonify({"message": "Error al actualizar el perfil"}), 400

        return jsonify({"message": "Perfil actualizado con éxito"}), 200

