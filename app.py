import os
from flask import Flask, request, jsonify
import bcrypt
import pymysql
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)  # Esto permitirá que cualquier origen pueda hacer solicitudes a tu servidor

# Función para crear la conexión con la base de datos MySQL
def create_connection():
    return pymysql.connect(
        host='bzfd6hwcfpo8wix0ovtb-mysql.services.clever-cloud.com',
        user='ujqw6wjpc7ndaw9w',
        password='GZKuuDdhcJzJOfoHM7x5',
        db='bzfd6hwcfpo8wix0ovtb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        correo = data.get('correo')
        contraseña = data.get('contraseña')

        # Verificar si los datos se están recibiendo correctamente
        user = verify_user_password(correo, contraseña)

        if user:
            # Eliminar la contraseña hasheada de la respuesta antes de enviarla
            user_data = user.copy()  # Crear una copia del usuario
            del user_data['contraseña']  # Eliminar la contraseña

            # Enviar solo los datos del usuario sin la contraseña
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": user_data,
                "redirect": "https://angelatovars.github.io/proyecto-autodidacta-frontend/index.html"  # Ruta absoluta para redirigir al frontend
            }), 200
        else:
            return jsonify({"message": "Correo o contraseña incorrectos"}), 401  # 401 para credenciales incorrectas
    except Exception as e:
        print("Error en la solicitud:", str(e))
        return jsonify({"message": "Error interno en el servidor", "error": str(e)}), 500


@app.route('/api/profile', methods=['GET'])
def obtener_perfil():
    correo = request.args.get('correo')
    user = get_user_by_email(correo)
    
    if user:
        # Devolver los datos del perfil del usuario (sin contraseña)
        user_data = {
            'nombre': user['nombre'],
            'correo': user['correo'],
            'edad': user['edad'],
            'tema_preferido': user['tema_preferido'],
            'nivel_preferido': user['nivel_preferido']
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


@app.route('/api/auth/admin', methods=['GET'])
def admin_panel():
    try:
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token no proporcionado"}), 403

        # Verificar el token básico para admin
        if token == "Bearer admin_token":
            return jsonify({"message": "Acceso permitido"}), 200
        else:
            return jsonify({"message": "No eres administrador"}), 403
    except Exception as e:
        print("Error en la autorización:", str(e))
        return jsonify({"message": "Error en la autorización", "error": str(e)}), 500

@app.route('/api/auth/verificar-admin', methods=['GET'])
def verificar_admin():
    try:
        correo = request.args.get('correo')
        
        if not correo:
            return jsonify({"message": "Correo no proporcionado"}), 400

        connection = create_connection()
        with connection.cursor() as cursor:
            query = "SELECT is_admin FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()

            if user and user['is_admin'] == 1:
                return jsonify({"message": "Es administrador"}), 200
            else:
                return jsonify({"message": "No es administrador"}), 403
    except Exception as e:
        print("Error al verificar admin:", str(e))
        return jsonify({"message": "Error interno", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/admin/estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            # Consultas para obtener estadísticas
            cursor.execute("SELECT COUNT(*) as totalUsuarios FROM usuarios")
            total_usuarios = cursor.fetchone()['totalUsuarios']

            cursor.execute("SELECT COUNT(*) as usuariosActivos FROM usuarios WHERE ultima_actividad > DATE_SUB(NOW(), INTERVAL 30 DAY)")
            usuarios_activos = cursor.fetchone()['usuariosActivos']

            cursor.execute("SELECT COUNT(*) as nuevosUsuarios FROM usuarios WHERE fecha_registro > DATE_SUB(NOW(), INTERVAL 30 DAY)")
            nuevos_usuarios = cursor.fetchone()['nuevosUsuarios']

            return jsonify({
                "totalUsuarios": total_usuarios,
                "usuariosActivos": usuarios_activos,
                "nuevosUsuarios": nuevos_usuarios
            }), 200
    except Exception as e:
        print("Error al obtener estadísticas:", str(e))
        return jsonify({"message": "Error al obtener estadísticas", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/admin/ranking', methods=['GET'])
def obtener_ranking_usuarios():
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            # Consulta para obtener ranking de usuarios 
            # Puedes ajustar esta consulta según tus necesidades específicas
            query = """
            SELECT 
                nombre, 
                correo, 
                COALESCE(puntos_totales, 0) as puntosTotales, 
                COALESCE(nivel, 'Sin nivel') as nivel, 
                ultima_actividad as ultimaActividad
            FROM usuarios
            ORDER BY puntos_totales DESC
            LIMIT 10
            """
            cursor.execute(query)
            ranking = cursor.fetchall()

            return jsonify(ranking), 200
    except Exception as e:
        print("Error al obtener ranking:", str(e))
        return jsonify({"message": "Error al obtener ranking", "error": str(e)}), 500
    finally:
        connection.close()
@app.route('/api/profile', methods=['PUT'])
@app.route('/api/admin/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            # Consulta para obtener todos los usuarios con información completa
            query = """
            SELECT 
                nombre, 
                correo, 
                edad, 
                fecha_registro, 
                is_admin, 
                tema_preferido, 
                nivel_preferido, 
                ultima_actividad 
            FROM usuarios
            ORDER BY fecha_registro DESC
            """
            cursor.execute(query)
            usuarios = cursor.fetchall()

            return jsonify(usuarios), 200
    except Exception as e:
        print("Error al obtener usuarios:", str(e))
        return jsonify({"message": "Error al obtener usuarios", "error": str(e)}), 500
    finally:
        connection.close()
def actualizar_perfil():
    correo = request.args.get('correo')
    data = request.get_json()
    
    # Imprimir los datos recibidos para debug
    print(f"Datos recibidos: {data}")

    # Validar si los datos necesarios están presentes
    if not all(key in data for key in ('nombre', 'edad', 'tema_preferido', 'nivel_preferido')):
        return jsonify({'message': 'Faltan datos para actualizar el perfil'}), 400

    user = get_user_by_email(correo)
    if user:
        update_user_profile(correo, data)
        return jsonify({'message': 'Perfil actualizado con éxito'}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('correo')
        contraseña = data.get('contraseña')
        edad = data.get('edad')

        # Verificar si el correo ya está registrado
        if check_email_exists(correo):
            return jsonify({"message": "El correo ya está registrado"}), 400

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        # Crear un nuevo usuario en la base de datos
        create_new_user(nombre, correo, hashed_password, edad)

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        print("Error en el registro:", str(e))
        return jsonify({"message": "Error al registrar el usuario", "error": str(e)}), 500


def verify_user_password(correo, contraseña):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(contraseña.encode('utf-8'), user['contraseña'].encode('utf-8')):
                return user
            return None
    except Exception as e:
        print("Error al verificar usuario:", str(e))
        return None
    finally:
        connection.close()
def update_user_points(correo, puntos_ganados):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = """
                UPDATE usuarios
                SET puntos_totales = puntos_totales + %s
                WHERE correo = %s
            """
            cursor.execute(query, (puntos_ganados, correo))
            connection.commit()
    except Exception as e:
        print("Error al actualizar puntos:", str(e))
    finally:
        connection.close()

@app.route('/api/actividad_restringida', methods=['GET'])
def actividad_restringida():
    correo = request.args.get('correo')

    if not correo:
        return jsonify({"message": "Correo no proporcionado"}), 400

    # Obtener los puntos del usuario
    user = get_user_by_email(correo)

    if user:
        puntos_totales = user['puntos_totales']

        # Verificar si el usuario tiene suficientes puntos
        if puntos_totales >= 100:  # Ajusta este valor según lo que necesites
            return jsonify({"message": "Acceso permitido a la actividad"}), 200
        else:
            return jsonify({"message": "No tienes suficientes puntos para acceder a esta actividad"}), 403
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

def get_user_by_email(correo):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            user = cursor.fetchone()
            return user
    except Exception as e:
        print("Error al obtener usuario:", str(e))
        return None
    finally:
        connection.close()


def check_email_exists(correo):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()
            return result['COUNT(*)'] > 0
    except Exception as e:
        print("Error al verificar correo:", str(e))
        return False
    finally:
        connection.close()


def create_new_user(nombre, correo, contraseña, edad):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = "INSERT INTO usuarios (nombre, correo, contraseña, edad) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, correo, contraseña, edad))
            connection.commit()
    except Exception as e:
        print("Error al crear usuario:", str(e))
    finally:
        connection.close()


def update_user_profile(correo, data):
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            query = """
                UPDATE usuarios 
                SET nombre = %s, edad = %s, tema_preferido = %s, nivel_preferido = %s 
                WHERE correo = %s
            """
            cursor.execute(query, (data['nombre'], data['edad'], data['tema_preferido'], data['nivel_preferido'], correo))
            connection.commit()
            print(f"Filas afectadas: {cursor.rowcount}")  # Mostrar cuántas filas fueron afectadas
    except Exception as e:
        print("Error al actualizar perfil:", str(e))
    finally:
        connection.close()




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
