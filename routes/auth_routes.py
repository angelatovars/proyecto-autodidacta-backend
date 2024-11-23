from flask import Blueprint, app, request, jsonify
from flask_cors import CORS
from settings.admin_config import AdminConfig
from controllers.auth_controller import AuthController
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user_model import UserModel

api = Blueprint("auth", __name__)


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    edad = data.get("edad")
    return AuthController.register(nombre, correo, contraseña, edad)


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    return AuthController.login(correo, contraseña)


@api.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    return AuthController.change_password()


@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return AuthController.logout()


@api.route("/verificar-correo", methods=["POST"])
def verificar_correo():
    data = request.get_json()
    correo = data.get("correo")
    usuario = UserModel.get_user_by_email(correo)

    return jsonify({"existe": usuario is not None})


@api.route("/admin", methods=["GET"])
@jwt_required()
def admin_endpoint():
    current_user_email = get_jwt_identity()
    if current_user_email == AdminConfig.ADMIN_ID:
        return jsonify({"message": "Admin"}), 200
    else:
        return jsonify({"error": "Invalid"}), 403
