from flask import request,jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required, get_jwt
from models.user_model import UserModel
from models.profile_model import ProfileModel
from utils.bcrypt_utils import hash_password, check_password
from utils.db_config import create_connection

class AuthController:
    @staticmethod
    def register(nombre, correo, contraseña, edad):
        # Cifrar la contraseña antes de guardarla
        contraseña_cifrada = hash_password(contraseña)

        # Crear el usuario
        user_id = UserModel.create_user(nombre, correo, contraseña_cifrada, edad)

        if user_id:
            # Crear el perfil asociado
            ProfileModel.create_profile(user_id)
            return jsonify({"message": "Usuario registrado con éxito y perfil creado"}), 201
        else:
            return jsonify({"message": "Error al registrar usuario"}), 500

    @staticmethod
    def login(correo, contraseña):
        user = UserModel.get_user_by_email(correo)

        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        if not check_password(contraseña, user['contraseña']):  # user['contraseña'] debe ser accesible
            return jsonify({"message": "Contraseña incorrecta"}), 401

        access_token = create_access_token(identity=user['id_usuario'])
        return jsonify({"access_token": access_token}), 200
    
    @staticmethod
    @jwt_required()  # Requiere que el usuario esté autenticado
    def logout():
        jti = get_jwt()["jti"]  # "jti" es el identificador único del token JWT
        connection = create_connection()

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO RevokedTokens (jti) VALUES (%s)"
                cursor.execute(query, (jti,))
                connection.commit()
            return {"message": "Sesión cerrada correctamente."}, 200
        except Exception as e:
            print(f"Error al revocar el token: {e}")
            return {"message": "Error al cerrar sesión."}, 500
        finally:
            connection.close()

    def change_password():
            user_id = get_jwt_identity()  # Obtener el ID del usuario a partir del token
            data = request.get_json()

            # Verificar que las contraseñas estén presentes en los datos
            if 'old_password' not in data or 'new_password' not in data:
                return jsonify({"message": "Faltan datos"}), 400

            old_password = data['old_password']
            new_password = data['new_password']

            # Obtener los datos del usuario desde la base de datos
            user = UserModel.get_user_by_id(user_id)

            if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404

            # Verificar que la contraseña actual sea correcta
            if not check_password(old_password, user['contraseña']):
                return jsonify({"message": "Contraseña actual incorrecta"}), 401

            # Hashear la nueva contraseña
            new_password_hashed = hash_password(new_password)

            # Actualizar la contraseña en la base de datos
            success = UserModel.update_password(user_id, new_password_hashed)

            if success:
                return jsonify({"message": "Contraseña actualizada correctamente"}), 200
            else:
                return jsonify({"message": "Error al actualizar la contraseña"}), 500

