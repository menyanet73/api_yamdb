import csv

from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Import csv file'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        file = options['file']
        path = f'static/data/{file}'
        with open(path, newline='') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                print(row)
                Category.objects.create(name=row[1], slug=row[2])
