# Телегоша

![tests workflow](https://github.com/deevgeny/telegosha/actions/workflows/tests_workflow.yaml/badge.svg)
![CI/CD workflow](https://github.com/deevgeny/telegosha/actions/workflows/ci_cd_workflow.yaml/badge.svg)

Школьный помощник для запоминания иностранных слов.

## О проекте
Телегоша - это веб приложение помогающее учить иностранные слова.
Специально спроектировано для использования в рамках школьной программы для
начальных классов. Основной принцип заключается в поэтапном прохождении
заданий.Преподаватель создает новую тему и добавляет к ней список слов, 
обязательных для изучения. Ученики последовательно выполняют задания по 
изучению новых слов посредством телеграм бота. Преподаватель следит за 
результатами выполнения заданий. 

## Стек технологий
* python 3.10.6
* django 4.1.6
* celery 5.2.7
* aiogram 2.24
* redis 7.0
* postrgesql 13.0
* nginx 1.21.3
* espeak 1.48.15
* ffmpeg 4.4.2

## Инфраструктура
Телегоша - это многоконтейнерное веб приложение, которое состоит из следующих
компонентов:
* database - база данных PostgreSQL
* redis - база данных Redis
* backend - веб приложение Django
* celery - очередь задач
* bot - телеграм бот
* nginx - обратный прокси-сервер

## Особенности процесса изучения слов
* При создании новой темы в которую добавлены школьные группы или  при 
добавлении школьной группы к уже существующей теме, для каждого пользователя 
группы создается первое задание - знакомство.
* Для изучения слов каждой отдельной темы существует определенная 
последовательность заданий: знакомство, запоминание, тест, правописание.
* При успешном завершении  текущего задания, следуещее задание создается 
автоматически.
* При успешном завершении всех заданий, тема считается пройденной.
* При добавлении нового иностранного слова, автоматически происходит генерация
mp3 файла с его произношением. Этот файл используется в первом задании
для изучения произношения. Текущая версия пока работает только с английскими
словами.

## Как запустить проект на сервере
1. Перед запуском проекта необходимо подготовить .env файл с переменными. В 
папке ifra есть пример такого файла:
```
# Backend & database settings
POSTGRES_USER=<your postres username>
POSTGRES_PASSWORD=<your password>
# Backend settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<your postgres database name>
DB_HOST=database
DB_PORT=5432
SECRET_KEY=<your django secret key>
DEBUG=0
ALLOWED_HOSTS=127.0.0.1 backend # Add server ip here when deployed
# Bot settings
TG_API_TOKEN=<your telegram bot token>
BACKEND_URL=http://backend:8000/api/v1/
# Celery settings
CELERY_BROKER_URL=redis://redis:6379/
```

2. Изменить настройки файла nginx.conf заменив ip адрес 127.0.0.1 на доменное 
имя или ip адрес сервера. Так как текущая версия работает с Telgram Bot API 
через обычный поллинг, то дополнительная настройка https не требуется. 
```
server {
    server_tokens off;
    server_name 127.0.0.1;
    listen 80;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    location /static/ {
        autoindex on;
        alias /app/static/;
    }

    location /media/ {
        autoindex on;
        alias /app/media/;
    }

    location /admin/ {
        proxy_set_header        Host $host;
        proxy_set_header        X-Forwarded-Host $host;
        proxy_set_header        X-Forwarded-Server $host;
        proxy_pass http://backend:8000/admin/;
    }
} 
```

3. Скопировать файлы из папки infra (nginx.conf, docker-compose.yaml, .env) на
сервер:
```sh
scp nginx.conf docker-compose.yaml .env username@host:~
```

4. Установить на сервере библиотеки для генерации звуковых файлов:
```sh
sudo apt-get update && apt-get install -y espeak ffmpeg
```

5. Запустить проект на сервере:
```sh
sudo docker-compose up -d
```

6. В контейнере бэкэнда собрать статику, выполнить миграции и создать
суперпользователя.
```sh
sudo docker-compose exec -T backend python manage.py makemigrations
sudo docker-compose exec -T backend python manage.py migrate
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
sudo docker-compose exec -T backend python manage.py create_admin \
--username <your username> \
--email <your email> \
--password <your password> 
```

7. Зайти на админ сайт проекта с данными суперпользователя

http://ваш-ip-или-домен/admin/
