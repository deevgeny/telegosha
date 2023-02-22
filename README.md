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

## Инфраструктура
Телегоша - это многоконтейнерное веб приложение, которое состоит из следующих
компонентов:
* database - база данных PostgreSQL
* redis - база данных Redis
* backend - веб приложение Django
* celery - очередь задач
* bot - телеграм бот
* nginx - обратный прокси-сервер

