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
    "user": 'LinkMDQ',
    'password': '155722Asd',
    'host': 'LinkMDQ.mysql.pythonanywhere-services.com',
    'database': 'favoritecake_db'
}

conexion = mysql.connector.connect(**config_dev)

