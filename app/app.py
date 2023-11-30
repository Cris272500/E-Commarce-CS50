from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt


from models import usuario, db, vendedores

import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Proyecto.db'  # 'sqlite:///site.db' indica que se usará SQLite y el archivo de la base de datos será 'site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar el seguimiento de modificaciones
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia a una clave secreta segura
bcrypt = Bcrypt(app)
db.init_app(app)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

#app.debug = True

@app.route("/", methods=["GET", "POST"])
def index():
    # Obteniendo id y name de la sesion
    id = session.get('user_id', None)
    name = session.get('user_name', None)

    # Verificamos si ha iniciado sesion
    if id is None or name is None:
        print("Hola")
        return render_template("index.html")
    else:
        mensaje = request.args.get('mensaje', None)
        estado = request.args.get('estado', None) 
        return render_template("index.html", mensaje=mensaje, estado=estado, name=name)

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
        
        # Hasheamos la password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
        # Crear un nuevo usuario y agregarlo a la base de datos
            nuevo_usuario = usuario(nombre=name, email=correo, password_hash=password_hash, direccion=direccion)
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

# Iniciar sesion comprador, usuario
@app.route("/comprador_login", methods=["GET", "POST"])
def comprador_login():
    if request.method == "POST":
        correo = request.form.get('email')
        password = request.form.get('password')

        usuario_existe = usuario.query.filter_by(email=correo).first()

        # Validando que el usuario existe
        if usuario_existe and bcrypt.check_password_hash(usuario_existe.password_hash, password):
            mensaje = "Inicio de sesion exitosamente"
            estado = "success_log"
            session['user_id'] = usuario_existe.id
            session['user_name'] = usuario_existe.nombre
            return redirect(f'/?mensaje={mensaje}&estado={estado}')
        else:
            mensaje = "El usuario no existe"
            estado = "error_log"
            return redirect(f'/comprador_login?mensaje={mensaje}&estado={estado}')
    else:
        mensaje = request.args.get('mensaje', None)
        estado = request.args.get('estado', None) 
        return render_template("login.html", mensaje=mensaje, estado=estado)

@app.route("/vendedor", methods=["GET", "POST"])
def vendedor():
    if request.method == "GET":
        mensaje = request.args.get('mensaje', None)
        estado = request.args.get('estado', None)
        return render_template("register.html", mensaje=mensaje, estado=estado)
    else:
        # obteniendo campos
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        password = request.form.get("contra")
        telefono = int(request.form.get("numero"))
        dir = request.form.get("direccion")

        # Hasheamos la password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # validando que el correo no existe en la clase usuario
        nuevo_vendedor = usuario.query.filter_by(email = correo).first()

        if (nuevo_vendedor):
           print("Waos")
           mensaje = "El correo ya existe en vendedores"
           estado = "error"
           return redirect(f'/vendedor?mensaje={mensaje}&estado={estado}')
        
        try:
            nuevo_vendedor = vendedores(nombre_vendedor=nombre, email_vendedor=correo, password_hash=password_hash, direccion_vendedor=dir, telefono=telefono)
            db.session.add(nuevo_vendedor)
            db.session.commit()
            mensaje = "Vendedor registrado exitosamente"
            estado = "success"
        except IntegrityError:
            db.session.rollback()
            mensaje = "Hubo un error"
            estado = "error"
        except Exception:
            db.session.rollback()
            mensaje = "Hubo un error"
            estado = "error"
        finally:
            db.session.close()
        return redirect(f'/vendedor?mensaje={mensaje}&estado={estado}')

#Cerrar sesion para el comprador
@app.route('/comprador_logout')
def comprador_logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    
    return redirect('/')

# Main
if __name__ == '__main__':
    app.run(debug=True, port=5000)