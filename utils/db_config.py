import pymysql

def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='app_didacta_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
