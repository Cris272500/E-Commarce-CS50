import os
import re

directory = 'templates'  # Cambia esto a tu directorio de plantillas

def cambiar_rutas_en_archivo(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        # Utiliza expresiones regulares para buscar y reemplazar las rutas
        content = re.sub(r'src="themes/images/products/', 'src="{{ url_for("static", filename="themes/images/products/', content)
    with open(filepath, 'w') as file:
        file.write(content)

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        cambiar_rutas_en_archivo(filepath)
