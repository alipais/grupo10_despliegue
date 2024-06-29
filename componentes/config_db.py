import mysql.connector

config_dev = {
    # configuración en desarrollo (local)
    "user": 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'favorite_cake'
}

config_prod = {
    # configuración en producción (despliegue)
    "user": 'liciaG',
    'password': 'grupo102024',
    'host': 'AliciaG.mysql.pythonanywhere-services.com',
    'database': 'AliciaG$favorite_cake'
}

conexion = mysql.connector.connect(**config_dev)

