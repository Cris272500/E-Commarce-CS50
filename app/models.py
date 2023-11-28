from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de la base de datos
class usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password_hash = db.Column(db.String(15), nullable = False)
    direccion = db.Column(db.String(120), nullable = False)