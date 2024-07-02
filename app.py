from flask import Flask, render_template, request, redirect, flash, url_for
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode
from componentes.validador import validar_contraseña, validar_nombre, validar_apellido
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ""}})
app.secret_key = 'clave'

# Configuración de la base de datos
db_config = {
    "user": 'LinkMDQ',
    'password': '155722Asd!',
    'host': 'LinkMDQ.mysql.pythonanywhere-services.com',
    'database': 'LinkMDQ$favoritecake_db'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    edad = request.form['edad']
    email = request.form['email']
    password = request.form['password']

    # Validar la contraseña
    valid, message = validar_contraseña(password)
    if not valid:
        flash(message)
        return redirect('/registro')

    # Validar el nombre
    valid, message = validar_nombre(nombre)
    if not valid:
        flash(message)
        return redirect('/registro')
    valid, message = validar_apellido(apellido)
    if not valid:
        flash(message)
        return redirect('/registro')

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Guardar el usuario en la base de datos
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios_ (nombre, apellido, edad, email, password) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, apellido, edad, email, hashed_password))
        conn.commit()
        flash("Usuario registrado exitosamente!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            flash("Algo está mal con tu usuario o contraseña de la base de datos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            flash("La base de datos no existe.")
        else:
            flash(f"Error: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect('/registro')
    
    
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        # Actualizar el usuario en la base de datos
        cursor.execute("""
            UPDATE usuarios SET nombre = %s, apellido = %s, email = %s
            WHERE id_usuario = %s
        """, (nombre, apellido, email, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario actualizado exitosamente!")
        return redirect('/usuarios')
    else:
        # Obtener los datos del usuario para mostrarlos en el formulario de edición
        cursor.execute("SELECT nombre, apellido, email FROM usuarios WHERE id_usuario = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_user.html', usuario=usuario, user_id=user_id)    


@app.route('/usuarios')
def usuarios():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, edad, email FROM usuarios_")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios_ WHERE id = %s", (user_id,))
        conn.commit()
        flash("Usuario eliminado exitosamente!")
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect('/usuarios')

if __name__ == '__main__':
    app.run(debug=True, port=5050)