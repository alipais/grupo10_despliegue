from flask import Flask, request, jsonify
from flask_cors import CORS
from componentes.config_db import conexion

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})  # Permitir CORS para las rutas que empiezan con /api/

# Conexión a la base de datos
def obtener_conexion():
    con = conexion
    try:
        cursor = con.cursor(dictionary=True)
        print('Conectada!')
    except Exception as e:
        print(f"Error al conectar: {e}")
        con.connect()
        cursor = con.cursor(dictionary=True)
        print('Reconectada!')
    return con, cursor

# Crear un nuevo usuario
@app.route('/api-favorite_cake/usuarios', methods=['POST'])
def crear_usuario():
    try:
        con, cursor = obtener_conexion()
        nuevo_usuario = request.json
        print("Datos del nuevo usuario:", nuevo_usuario)  # Agregar mensaje de depuración
        consulta = """
        INSERT INTO usuarios (nombre, apellido, email, contraseña, activo, administrador)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (
            nuevo_usuario['nombre'], 
            nuevo_usuario['apellido'], 
            nuevo_usuario['email'], 
            nuevo_usuario['contraseña'], 
            nuevo_usuario['activo'], 
            nuevo_usuario['administrador']
        ))
        con.commit()
        con.close()
        return jsonify({"mensaje": "Usuario creado exitosamente!"}), 201
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return jsonify({"error": "Ocurrió un error al crear el usuario"}), 500

if __name__ == '__main__':
    app.run(debug=True)

