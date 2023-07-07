import os
import django
from django.core.files import File

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jardineando_projecto.settings')
django.setup()

from api.models import OnePieceCapituloManga as prueba
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

        volume = item['Volume']
        image_path = f'F:/one/onepiece-vol-{volume:03}.jpg'  # Format the volume number with leading zeros

        manga = prueba(
            capitulo=item['Chapter_Number'],
            volumen=volume,
            titulo=item['Name'],
            titulo_romanizado=item['Romanized_title'],
            titulo_viz=item['Viz_title'],
            paginas=paginas,
            fecha_publicacion=fecha_publicacion,
            episodios=item['Episodes']
        )

        # Open the image file and assign it to the manga object
        with open(image_path, 'rb') as image_file:
            manga.imagen.save(os.path.basename(image_path), File(image_file))

        manga.save()

    print("Import successful!")

if __name__ == '__main__':
    import_json()
