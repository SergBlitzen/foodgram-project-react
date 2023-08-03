# Foodgram

Продуктовый помощник — SPA, на котором можно размещать свои рецепты и смотреть чужие, а также добавлять в избранное и корзину, которую можно выгрузить файлом.

## Адрес и доступ:
URL: fdgrm.ddns.net<br>
Admin username: foodgram_admin<br>
Admin password: password

### Запуск проекта
Приложение запускается в docker-контейнерах, для чего подготовлен файл docker-compose.yml в директории infra.<br>
Последовательность запуска:<br>
— запустить docker compose из директории infra<br>
```docker compose up --build```<br>
— провести миграции в контейнере с бэкендом<br>
```docker compose exec backen python manage.py migrate```<br>
— (дополнительно) Загрузить в базу образец данных ингредиентов:<br>
```docker compose exec backend python manage.py import_data```<br>

Для запуска необходимы переменные окружения файла .env в директории infra. Пример заполнения:<br>
POSTGRES_USER=string<br>
POSTGRES_PASSWORD=string<br>
POSTGRES_DB=string<br>
DB_HOST=string<br>
DB_PORT=integer<br>
SECRET_KEY=string<br>
DEBUG=boolean. Нужно иметь в виду, что любое нечисловое значение, попадающее в env_file, становится строкой.<br>
ALLOWED_HOSTS=string. Передать все хосты в строке через пробел, чтобы в settings отработал метод split(' ').


Для продакшена на удалённом сервере реализован файл docker-compose.production.yml с настроенным деплоем в Main Worflow с помощью GitHub Actions.
При необходимости развернуть проект вручную требуется разместить файл "docker-compose.production.yml" в нужной директории и выполнить следующие команды:
<br>— загрузить образы контейнеров из Docker Hub;
<br>```sudo docker compose -f docker-compose.production.yml pull```
<br>— остановить контейнеры;
<br>```sudo docker compose -f docker-compose.production.yml down```
<br>— запустить контейнеры в фоновом режиме;
<br>```sudo docker compose -f docker-compose.production.yml up -d```
<br>— выполнить миграции в контейнере бэкенда;
<br>```sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate```
<br>— собрать статику;
<br>```sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic```
<br>— скопировать статику.
<br>```sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/```


Backend and CI/CD by Serg Blitzen
Frontend by Yandex.Practicum
