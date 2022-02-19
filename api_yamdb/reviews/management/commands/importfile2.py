import csv, codecs, sqlite3

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
        with codecs.open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            firstrow = next(reader)
            reader.__next__()
            for raw in reader:
                if table_name in table_names:
                    table_name = table_names[table_name]
                # if table_name == 'genre_title':
                #     table_name = 'title_genre'
                # if table_name == 'users':
                #     table_name = 'user'
                if file == 'titles.csv':
                    # table_name = 'title'
                    if 'description' not in firstrow:
                        raw.insert(3, '')
                print(raw)
                print(f'INSERT INTO reviews_{table_name} VALUES {tuple(raw)}')
                cur.execute(f'INSERT INTO reviews_{table_name} VALUES {tuple(raw)};')
        con.commit()
        con.close()

table_names = {
    'genre_title': 'title_genre',
    'users': 'user',
    'titles': 'title',
}