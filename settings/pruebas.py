import secrets

# Generar una clave secreta aleatoria para Flask
secret_key = secrets.token_hex(32)  # Genera una clave de 64 caracteres
jwt_secret_key = secrets.token_hex(32)  # Genera una clave de 64 caracteres

print(f'SECRET_KEY = {secret_key}')
print(f'JWT_SECRET_KEY = {jwt_secret_key}')