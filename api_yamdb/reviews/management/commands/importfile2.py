import csv, codecs

from django.core.management.base import BaseCommand
from reviews.models import Category, Title, Review, User, Genre, Comment

class Command(BaseCommand):
    help = 'Import csv file'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        file = options['file']
        file_name = file.partition('.')[0]
        path = f'static/data/{file}'
        with codecs.open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            ''' Определение имен для орм команды '''
            model = model_names[f'{file_name}']
            method = 'create'
            if file_name == 'genre_title':
                method = 'update'

            ''' Определение полей указываемых в модели'''
            print(headers)
            for row in reader:
                fields = ''
                string_orm = ''
                for header, field in zip(headers,row):
                    if 'id'  in header or header in int_fields:
                        if header == 'category' or header == 'genre':
                            header += '_id'
                            print(header)
                    elif header == 'text':
                        field = f'"{field}"' # Нужно придумать как решить проблему с переносом строки в этом поле
                    else:
                        field = f'"{field}"'
                    fields += f'{header}={field}, '
                fields = fields[:-2] # Удалим последнюю запятую
                string_orm = f'{model}.objects.{method}({fields})'
                print(string_orm)
                exec(string_orm)
                # Category.objects.create(name=row[1], slug=row[2])

model_names = {
    'category': 'Category',
    'comments': 'Comment',
    'genre_title': 'Title',
    'genre': 'Genre',
    'review': 'Review',
    'titles': 'Title',
    'users': 'User',
}

int_fields = ['year', 'pub_date', 'category', 'genre', 'author', 'score']