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
    "user": 'Alipais',
    'password': 'grupo102024',
    'host': 'Alipais.mysql.pythonanywhere-services.com',
    'database': 'Alipais$favoriteCake'
}

conexion = mysql.connector.connect(**config_dev)

