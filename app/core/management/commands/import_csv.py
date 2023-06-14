from csv import DictReader
from django.core.management import BaseCommand

from core.models import CountryRank

class Command(BaseCommand):
    help = 'Import data from CSV file to database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = DictReader(file)

            for row in reader:
                CountryRank.objects.create(
                    year=row['Year'],
                    sector=row['Sector'],
                    subsector=row['Subsector'],
                    indicator=row['Indicator'],
                    amount=row['Amount'],
                    country=row['Country'],
                    rank=row['Rank']
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))