import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import OnePieceCapituloManga


class Command(BaseCommand):
    help = 'Imports manga data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                OnePieceCapituloManga.objects.create(
                    capitulo=row['Chapter_Number'],
                    volumen=row['Volume'],
                    titulo=row['Name'],
                    titulo_romanizado=row['Romanized_title'],
                    titulo_viz=row['Viz_title'],
                    paginas=row['Pages'],
                    fecha_publicacion=datetime.strptime(row['Date'], '%B %d, %Y').date(),
                    episodios=row['Episodes']
                )