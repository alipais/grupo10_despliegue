import mysql.connector

config_dev = {
    "user": 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'favorite_cake'
}

conexion = mysql.connector.connect(**config_dev)

