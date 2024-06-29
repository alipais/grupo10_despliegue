from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from componentes.config_db import conexion

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ""}})  # Permitir CORS para las rutas que empiezan con /api/

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
    return  cursor

@app.route('/')
def inicio():
    try:
        cursor = obtener_conexion()
        cursor.execute('SELECT * FROM usuarios;')
        datos = cursor.fetchall()
       # con.close()
        return render_template('usuarios/usuarios.html', usuarios=datos)
    except Exception as e:
        print(f"Error al cargar la página de inicio: {e}")
        return "Ocurrió un error al cargar la página de inicio"

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
    
@app.route('/api-favorite_cake/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        con, cursor = obtener_conexion()
        cursor.execute('SELECT * FROM usuarios;')
        datos = cursor.fetchall()
        con.close()
        return jsonify(datos)
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify({"error": "Ocurrió un error al obtener los usuarios"}), 500


if __name__ == '__main__':
    app.run(debug=True)

