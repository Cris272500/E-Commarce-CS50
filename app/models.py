from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

# Modelo de la base de datos
class usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = True)
    email = db.Column(db.String(120), nullable = True, unique = True)
    password_hash = db.Column(db.String(50), nullable = True)
    direccion = db.Column(db.String(120), nullable = True)

class categoria_product(db.Model):
    categoria_id = db.Column(db.Integer, primary_key = True)
    name_category = db.Column(db.String(20),nullable = True)

class productos(db.Model):
    product_id = db.Column(db.Integer, primary_key = True)
    nombre_producto = db.Column(db.String(20),nullable = True)
    Descripcion = db.Column(db.String(500),nullable = False)
    precio = db.Column(db.DECIMAL, nullable = True)
    stock = db.Column(db.Integer,nullable = True)
    categoria_id = db.Column(db.Integer,db.ForeignKey('categoria_product.categoria_id'), nullable = True)
    
class ordenes(db.Model):
    orden_id = db.Column(db.Integer,primary_key = True)
    cliente_id = db.Column(db.Integer, nullable = True)
    fecha_orden = db.Column(db.DateTime, nullable = True)
    estado = db.Column(db.String(10),nullable = True)
    
#class carrito(db.Model):
    #carrito_id = db.Column(db.Integer, primary_key = True)
    #cliente_id = db.Column(db.String(20),db.ForeignKey('usuario.cliente_id'), nullable = True)
    #product_id = db.Column(db.Integer,db.ForeignKey('productos.product'), nullable = True)
    
class pago(db.Model):
    pago_id = db.Column(db.Integer, primary_key = True, )
    metodo_pago = db.Column(db.String(25), nullable = True)
    pago_producto = db.Column(db.DECIMAL(25),nullable = True)
    
#class tarjetas(db.Model):
    #numero_tarjeta = db.Column(db.String(19), db.ForeignKey('pago.metodo_pago'), nullable = True, unique = True)
    #nombre_usuario = db.Column(db.String(50), db.ForeignKey('usuario.nombre_usuario'), nullable = True)
    #cvc = db.Column(db.Integer, nullable = True, unique = True)
    #correo = db.Column(db.String(50), db.ForeignKey('usuario.email'), nullable = True, unique = True)
    
#class recibo(db.Model):
    #id = db.Column(db.Integer, primary_key = True, unique = True)
    #usuario = db.Column(db.String(40), db.ForeignKey('usuario.id'), nullable = True, unique = True)
    #product_id = db.Column(db.String(20), db.ForeignKey('producto_id.carrito'), nullable = True)
    #fecha = db.Column(db.DateTime, nullable = True)
    #total = db.Column(db.DECIMAL, nullable = True)
    #pago_producto = db.Column(db.DECIMAL, db.ForeignKey('pago_product.pago'), nullable = True)
    
class vendedores(db.Model):
    id_vendedor = db.Column(db.Integer, primary_key = True)
    nombre_vendedor = db.Column(db.String(50), nullable = True)
    email_vendedor = db.Column(db.String(120), nullable = True, unique = True)
    password_hash = db.Column(db.String(15), nullable = True)
    direccion_vendedor = db.Column(db.String(120), nullable = True)    
    telefono = db.Column(db.Integer, nullable = True, unique = True)
    