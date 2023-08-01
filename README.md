# Foodgram

Продуктовый помощник — SPA, на котором можно размещать свои рецепты и смотреть чужие, а также добавлять в избранное и корзину, которую можно выгрузить файлом.


### Запуск проекта
Приложение запускается в docker-контейнерах, для чего подготовлен файл docker-compose.yml в директории infra.<br>
Последовательность запуска:<br>
— запустить docker compose из директории infra<br>
```docker compose up --build```<br>
— провести миграции в контейнере с бэкендом<br>
```docker compose exec backen python manage.py migrate```<br>
— (дополнительно) Загрузить в базу образец данных ингредиентов:<br>
```docker compose exec backend python manage.py import_data```<br>
<br>
Для запуска необходимы переменные окружения файла .env в директории infra. Пример заполнения:<br>
POSTGRES_USER=string<br>
POSTGRES_PASSWORD=string<br>
POSTGRES_DB=string<br>
DB_HOST=string<br>
DB_PORT=integer<br>
SECRET_KEY=string<br>
DEBUG=boolean. Нужно иметь в виду, что любое нечисловое значение, попадающее в env_file, становится строкой.<br>
