from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


from models import usuario, db

import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Proyecto.db'  # 'sqlite:///site.db' indica que se usará SQLite y el archivo de la base de datos será 'site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar el seguimiento de modificaciones

db.init_app(app)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

#app.debug = True

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = request.args.get('mensaje', None)
    estado = request.args.get('estado', None) 
    return render_template("index.html", mensaje=mensaje, estado=estado)

@app.route("/comprador", methods=["GET", "POST"])
def comprador():
    if request.method == "GET":
        conexion = sqlite3.connect('instance/Proyecto.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuario")

        # Obteniendo todos los registros
        registros = cursor.fetchall()
        print(f"Registros: {registros}")
        mensaje = request.args.get('mensaje', None)
        estado = request.args.get('estado', None) 
        return render_template("login.html", mensaje=mensaje, estado=estado)
    else:
        # Obteniendo campos
        name = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("contra")
        direccion = request.form.get("direcc")
        
        
        try:
        # Crear un nuevo usuario y agregarlo a la base de datos
            nuevo_usuario = usuario(nombre=name, email=correo, password_hash=password, direccion=direccion)
            db.session.add(nuevo_usuario)
            db.session.commit()
            mensaje = "Usuario registrado exitosamente"
            estado = "success"
        except IntegrityError as e:
            db.session.rollback()
            mensaje = "El correo ya está registrado"
            estado = "error"
        except Exception as e:
            db.session.rollback()
            mensaje = "Error al registrar usuario"
            estado = "error"
        finally:
            db.session.close()

        return redirect(f'/comprador?mensaje={mensaje}&estado={estado}')
        

@app.route("/vendedor", methods=["GET", "POST"])
def vendedor():
    if request.method == "GET":
        return render_template("register.html")
    else:
        pass
# Main
if __name__ == '__main__':
    app.run(debug=True, port=5000)