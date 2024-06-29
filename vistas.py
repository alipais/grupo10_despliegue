from flask import render_template
from app import app, obtener_conexion

@app.route('/')
def inicio():
    try:
        con, cursor = obtener_conexion()
        cursor.execute('SELECT * FROM usuarios;')
        datos = cursor.fetchall()
        con.close()
        return render_template('./usuarios/usuarios.html', usuarios=datos)
    except Exception as e:
        print(f"Error al cargar la página de inicio: {e}")
        return "Ocurrió un error al cargar la página de inicio"