import sqlite3

conn = sqlite3.connect('Proyecto.db')
print("Se conecto a la base de datos")

# Creamos la tabla usuarios
conn.execute(
    "CREATE TABLE IF NOT EXISTS MetodosPago("
             "id_metodo_pago INTEGER PRIMARY KEY NOT NULL,"
             "id_usuario INTEGER NOT NULL,"
             "tarjeta_tipo TEXT NOT NULL,"
             "num_tarjeta TEXT NOT NULL,"
             "FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)"
    ")"
)
conn.close()
