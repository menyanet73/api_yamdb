import csv, sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import csv file, genre_title files import will be after title and genre files'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        file = options['file']
        path = f'static/data/{file}'
        table_name = file.partition('.')[0]
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(path, newline='') as f:
            reader = csv.reader(f)
            reader.__next__()
            for raw in reader:
                print(tuple(raw))
                if table_name == 'genre_title':
                    table_name = 'title_genre'
                cur.execute(f'INSERT INTO reviews_{table_name} VALUES {tuple(raw)}')
        con.commit()
        con.close()
