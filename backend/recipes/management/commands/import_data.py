import codecs
import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient

data_dir = settings.BASE_DIR.parent / 'data'  # /foodgram-project-react/data
file_list = os.listdir(data_dir)


class Command(BaseCommand):
    """Команда для импорта данных об ингредиентах из CSV-файла."""
    help = 'Команда для импорта данных.'

    def handle(self, *args, **options):
        model = Ingredient
        for file in file_list:
            if file.endswith('.csv'):
                with codecs.open(
                        str(data_dir) + '/' + file, 'r', 'utf-8'
                ) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        try:
                            model.objects.get_or_create(
                                name=row[0], measurement_unit=row[1]
                            )
                            self.stdout(f'Добавлены данные: {row}')
                        except Exception:
                            self.stdout(f'Данные не добавлены: {row}')
