import bcrypt
import sqlite3

# Función para conectarse a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('app_didacta_bd.db')  # Conexión a la base de datos
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas como diccionarios
    return conn

# Función para crear la tabla de usuarios (si no existe)
def crear_tabla_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            tema_preferido TEXT NOT NULL,
            nivel_preferido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para buscar usuario por correo
def buscar_usuario_por_correo(correo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
    user = cursor.fetchone()  # Obtiene el primer usuario que coincida con el correo
    conn.close()
    if user:
        return dict(user)  # Retorna el usuario como un diccionario
    return None

# Función para verificar la contraseña
def verify_user_password(correo, contraseña):
    user = buscar_usuario_por_correo(correo)
    if user:
        # Verificar la contraseña hasheada
        if bcrypt.checkpw(contraseña.encode('utf-8'), user['contraseña'].encode('utf-8')):
            return user
    return None  # Si no existe el usuario o la contraseña no coincide

# Función para registrar un nuevo usuario
def registrar_usuario(correo, contraseña, nombre, edad, tema_preferido, nivel_preferido):
    # Verificar si el correo ya existe
    if buscar_usuario_por_correo(correo):
        return f"Error: El correo '{correo}' ya está registrado."

    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (correo, contraseña, nombre, edad, tema_preferido, nivel_preferido) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (correo, hashed_password, nombre, edad, tema_preferido, nivel_preferido))
    conn.commit()
    conn.close()
    return f"Usuario con correo '{correo}' registrado correctamente."

# Función para actualizar la información de un usuario
def actualizar_perfil(correo, nombre, edad, tema_preferido, nivel_preferido):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios 
        SET nombre = ?, edad = ?, tema_preferido = ?, nivel_preferido = ? 
        WHERE correo = ?
    ''', (nombre, edad, tema_preferido, nivel_preferido, correo))
    conn.commit()
    conn.close()
    return f"Perfil de '{correo}' actualizado correctamente."

# Crear la tabla al iniciar el programa
crear_tabla_usuarios()

# Ejemplo de cómo registrar un nuevo usuario
# Se omite el ejemplo de registrar usuario para producción, ya que puede manejarse desde el frontend.
# registrar_usuario('usuario@ejemplo.com', 'contraseñaSegura123', 'Juan Pérez', 30, 'Matemáticas', 'Intermedio')

# Ejemplo de cómo verificar un usuario
correo_input = input("Ingresa el correo: ")
contraseña_input = input("Ingresa la contraseña: ")
usuario = verify_user_password(correo_input, contraseña_input)

if usuario:
    print(f"Usuario encontrado: {usuario['nombre']} ({usuario['correo']})")
else:
    print("Usuario no encontrado o contraseña incorrecta")

# Ejemplo de cómo actualizar el perfil de un usuario
# actualizar_perfil('usuario@ejemplo.com', 'Juan Pérez', 31, 'Física', 'Avanzado')
