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

nginx контейнер обрабатывает запросы к админ сайту для администрирования 
приложения, а так же раздает медиа и статику. Все остальное взаимодействие 
между ботом и бэкэндом происходит внутри докера. Пользователи идентифицируются 
по телеграм id. Бот делает запросы на API бэкэнда и получает результаты. В 
данный момент реализованы следующие эндпоинты:

GET /api/v1/tasks/telegram_id/ - получить задания пользователя

PATCH /api/v1/tasks/telegram_id/task_id/ - обновить результат задания
{"incorrect": 0,
 "correct": 10}

GET /api/v1/progress/telegram_id/ - получить результаты пользователя


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

## Способы запуска проекта
В папке infra собрана коллекция файлов для различных способов запуска проекта.
- Работа через http протокол с ip адресом или доменным именем и обычным
поллингом
  - http_nginx.conf
  - http-docker-compose.yaml
- Работа через https протокол c доменным именем и вебхуком
  - https_nginx.conf
  - https-docker-compose.yaml
- Генерация ssl сертификата для домена
  - cert_nginx.conf
  - cert-docker-compose.yaml

## Генерация ssl сертификата
Перед запуском проекта через https протокол необходимо сначала сгенерировать 
 и установить ssl сертифика. 
Генерация сертификата происходит автоматически. Для этого достаточно один раз 
запустить контейнеры с помощью docker-compose файла.
1. Сначала необходимо скопировать файлы `cert_nginx.conf` и 
`cert-docker-compose.yaml` на сервер и переименовать их удалив префикс `cert`: 
```sh
scp cert_nginx.conf cert-docker-compose.yaml <username>@<server-ip>:~
```
2. Затем внести изменения в файлы `nginx.conf` и `docker-compose.yaml` в 
указанных местах:
```
# nginx.conf
...
server {
    listen 80;
    server_name _; # Replace _ with your domain name
...
}
# docker-compose.yaml
...
command: certonly --webroot -w /var/www/certbot --force-renewal --email {your email} -d {your domain} --agree-tos
...
```
3. После этого запустить контейнеры с выводом в терминал, чтобы можно было 
проконтролировать результат: 
```sh
sudo docker-compose up
```
4. В завершении контейнеры и файлы `nginx.conf` и `docker-compose.yaml` можно 
удалить, так как они больше не нужны:
```sh
sudo docker-compose down
rm nginx.conf docker-compose.yaml
```

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
ALLOWED_HOSTS=127.0.0.1 backend # Add server ip or domain here when deployed
CSRF_TRUSTED_ORIGINS=https://example.com # your domain name required when using https
# Bot settings
TG_API_TOKEN=<your telegram bot token>
WEBHOOK_HOST=https://example.com # your domain name required when using webhook
WEBHOOK_PATH=/example_path/ # required when using webhook, should be same as location in nginx.conf proxy_pass to bot container (http://bot:8000)
BACKEND_URL=http://backend:8000/api/v1/
# Celery settings
CELERY_BROKER_URL=redis://redis:6379/
```

2. Скопировать файлы выбранного метода запуска из папки infra
(*_nginx.conf, *-docker-compose.yaml, .env) на сервер: 
```sh
scp *_nginx.conf *-docker-compose.yaml .env username@host:~
```

3. Переименовать файлы удалив префикс способа запуска, чтобы в результате 
на сервере лежало три файла: `nginx.conf`, `docker-compose.yaml`, `.env`

4. Изменить настройки файла nginx.conf во всех указанных местах. В случае с 
https так же нужно внести корректировки в файл `docker-compose.yaml`. 
```
server {
    server_name _; # Replace _ with domain name or ip
    listen 80;
    ...
} 
```

5. Установить на сервере библиотеки для генерации звуковых файлов:
```sh
sudo apt-get update && apt-get install -y espeak ffmpeg
```

6. Запустить проект на сервере:
```sh
sudo docker-compose up -d
```

7. В контейнере бэкэнда собрать статику, выполнить миграции и создать
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

8. Зайти на админ сайт проекта с данными суперпользователя

http://ваш-ip-или-домен/admin/


## Обновление ssl сертификата

Для обновления ssl сертификата достаточно вручную в терминале выполнить 
команду:
```sh
sudo docker-compose up certbot
```

Или можно добавить эту задачу в cron, чтобы она выполнялась один раз в два 
месяца:
```sh
crontab -e

0 0 1 */2 * /usr/local/bin/docker-compose -f /home/<usename>/docker-compose.yaml up certbot
```