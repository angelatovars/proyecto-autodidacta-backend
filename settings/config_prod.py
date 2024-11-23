# config_prod.py
from config import Config
class ProdConfig(Config):
    DEBUG = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'DB_Final'
