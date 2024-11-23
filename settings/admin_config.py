from werkzeug.security import generate_password_hash

class AdminConfig:
    ADMIN_ID = 64
    ADMIN_EMAIL = 'admin@admin.com'
    ADMIN_PASSWORD = 'admin12345'
    ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)
    ADMIN_NAME = 'Admin'
    ADMIN_AGE = 100