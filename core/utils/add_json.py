import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jardineando_projecto.settings')
django.setup()

from api.models import OnePieceCapituloManga
import json
from datetime import datetime

def import_json():
    json_file = 'data.json'  # Replace with the actual path to your JSON file

    with open(json_file, 'r') as file:
        json_data = json.load(file)

    for item in json_data:
        fecha_publicacion = datetime.strptime(item['Date'], '%B %d, %Y').strftime('%Y-%m-%d')

        paginas = item['Pages']
        if paginas == 'NA':
            paginas = 0  # Set a default value or handle it as per your requirements

        manga = OnePieceCapituloManga(
            capitulo=item['Chapter_Number'],
            volumen=item['Volume'],
            titulo=item['Name'],
            titulo_romanizado=item['Romanized_title'],
            titulo_viz=item['Viz_title'],
            paginas=paginas,
            fecha_publicacion=fecha_publicacion,
            episodios=item['Episodes']
        )
        manga.save()

    print("Import successful!")

if __name__ == '__main__':
    import_json()
