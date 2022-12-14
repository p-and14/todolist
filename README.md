Todolist - список задач
========
________
#### *Веб-приложение планировщика задач*
________
## Stack:
- python3.10
- Django
- Postgres
___
## Project launch:
1. Создать виртуальное окружение.
2. Установить зависимости:
> pip install -r requirements.txt
3. Создать ".env" файл на примере ".env_example".
4. Создать БД:
   1. Установить к себе на компьютер по инструкции из [официальной документации](https://www.postgresql.org/download/). 
   2. Установить docker-контейнер с уже готовой и настроенной СУБД. 
    > docker run --name todolist-postgres -e POSTGRES_PASSWORD=postgres -d postgres
5. Создать миграцию для приложений:
> python manage.py makemigrations 
6. Применить все миграции:
> python manage.py migrate
7. Для запуска телеграм бота применить команду:
> python manage.py runbot

## Project launch with Docker:
1. Создать ".env" файл на примере ".env_example".
2. Запустить команду:
> docker-compose up -d --build
