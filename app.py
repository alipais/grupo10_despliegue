from flask import Flask, render_template, request, redirect, url_for, flash
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
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'favoritecake_db'
}

@app.route('/')
def index():
    return render_template('index.html')
########## registro usuario #######
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
#wtform
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
    
 ############## editar usuario #############
    
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        email = request.form['email']
        # Actualizar el usuario en la base de datos
        cursor.execute("""
            UPDATE usuarios_ SET nombre = %s, apellido = %s, edad = %s, email = %s
            WHERE id = %s
        """, (nombre, apellido, edad, email, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario actualizado exitosamente!")
        return redirect('/usuarios')
    else:
        # Obtener los datos del usuario para mostrarlos en el formulario de edición
        cursor.execute("SELECT nombre, apellido, edad, email FROM usuarios_ WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_user.html', usuario=usuario, user_id=user_id)
   


@app.route('/usuarios')
def usuarios():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, apellido, edad, email FROM usuarios_')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios_=usuarios)



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

##################### pedidos ############################

#ver pedidos

@app.route('/pedidos')
def verpedidos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT id_pedidos, id_usuario, tipo_evento, Cantidad_personas, nombre_contacto, apellido_contacto, email_contacto, telefono_contacto, mensaje FROM pedidos_')
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/delete_pedido/<int:pedido_id>', methods=['POST'])
def delete_pedido(pedido_id):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos_ WHERE id_pedidos = %s", (pedido_id,))
        conn.commit()
        flash("Pedido eliminado exitosamente!")
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

    return redirect('/pedidos')

@app.route('/contacto')
def consulta():
    return render_template('contacto.html')

@app.route('/contacto', methods=['POST'])
def realizar_pedido():
    nombre_contacto = request.form['nombre']
    apellido_contacto = request.form['apellido']
    email_contacto = request.form['email']
    telefono_contacto = request.form['telefono_contacto']
    Cantidad_personas = request.form['cantidad_personas']
    mensaje = request.form['consulta']
    tipo_evento = request.form['tipo_evento']

    # Guardar la consulta/pedido en la base de datos
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos_ (tipo_evento, Cantidad_personas, nombre_contacto, apellido_contacto, email_contacto, telefono_contacto, mensaje) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (tipo_evento, Cantidad_personas, nombre_contacto, apellido_contacto, email_contacto, telefono_contacto, mensaje))
        conn.commit()
        flash("Consulta/pedido registrado exitosamente!")
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

    return redirect('/contacto')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)



#SELECT 'id_pedidos, id_usuario, tipo_evento, Cantidad_personas, nombre_contacto, apellido_contacto, email_contacto, telefono_contacto, mensaje FROM pedidos');
