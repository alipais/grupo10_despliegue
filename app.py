from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode
from componentes.validador import validar_contraseña, validar_nombre
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ""}})
app.secret_key = 'clave'

# Configuración de la base de datos
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'favorite_cake'
}

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']

    # Validar la contraseña
    valid, message = validar_contraseña(password)
    if not valid:
        flash(message)
        return redirect('/registro')
    
    # Validar nombre
    valid, message = validar_nombre(nombre)
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
        cursor.execute("INSERT INTO usuarios (nombre, apellido, email, contraseña) VALUES (%s, %s, %s, %s)",
                       (nombre, apellido, email, hashed_password))
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

@app.route('/usuarios')
def usuarios():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, apellido, email FROM usuarios")
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
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
        conn.commit()
        flash("Usuario eliminado exitosamente!")
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect('/usuarios')
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])

def update_user(user_id):
    if request.method == 'GET':
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, apellido, email FROM usuarios WHERE id_usuario = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('update_user.html', usuario=usuario)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']

        conn = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nombre = %s, apellido = %s, email = %s WHERE id_usuario = %s",
                           (nombre, apellido, email, user_id))
            conn.commit()
            flash("Usuario actualizado exitosamente!")
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            if conn:
                cursor.close()
                conn.close()

        return redirect('/usuarios')




if __name__ == '__main__':
    app.run(debug=True)
