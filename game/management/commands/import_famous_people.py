from django.core.management.base import BaseCommand
import csv
from game.models import FamousPerson


class Command(BaseCommand):
    help = 'Imports data from a CSV file into the FamousPerson model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='Path to the CSV file containing the data')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                FamousPerson.objects.create(
                    name=row[0],
                    occupation=row[1],
                    gender=row[2],
                    alive=row[3] == 'TRUE',
                    bplace_name=row[4],
                    bplace_country=row[5],
                    birthdate=row[6],
                    birthyear=int(row[7]) if row[7] else None,
                    dplace_name=row[8],
                    dplace_country=row[9],
                    deathdate=row[10],
                    deathyear=int(row[11]) if row[11] else None,
                    age=int(row[12]) if row[12] else None,
                    hpi=float(row[13]) if row[13] else None
                )
