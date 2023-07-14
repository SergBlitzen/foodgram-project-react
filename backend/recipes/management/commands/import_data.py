import csv
import os
import codecs

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


data_dir = settings.BASE_DIR.parent / 'data'  # \foodgram-project-react\data
print(data_dir)
file_list = os.listdir(data_dir)
print(file_list)


class Command(BaseCommand):
    help = 'Команда для импорта данных.'

    def handle(self, *args, **options):
        model = Ingredient
        for file in file_list:
            if file.endswith('.csv'):
                with codecs.open(str(data_dir) + '/' + file, 'r', 'utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        try:
                            model.objects.get_or_create(name=row[0], measurement_unit=row[1])
                            print(f'Добавлены данные: {row}')
                        except Exception:
                            print(f'Данные не добавлены: {row}')
