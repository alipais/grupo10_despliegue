import mysql.connector

config_dev = {
    # configuración en desarrollo (local)
    "user": 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'favoritecake_db'
}

config_prod = {
    # configuración en producción (despliegue)
    "user": 'AliciaG',
    'password': 'grupo102024',
    'host': 'AliciaG.mysql.pythonanywhere-services.com',
    'database': 'AliciaG$favoriteCake'
}

conexion = mysql.connector.connect(**config_dev)

