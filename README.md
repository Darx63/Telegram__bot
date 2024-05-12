# Разворачиваем собственного телеграм бота с подключением к БД Postgres
В качестве начальных данных имеем:

-Написанный на Python бекенд телеграм бота. (Файл Bot.py)

-Виртуальная машина с ОС Linux Ubuntu 20.04 с установленным ПО Docker.

## Ход выполнения:
### Создаем кастомную сеть для связи контейнеров.
```shell
docker network create bot_random
```
### Поднимаем контейнер с Postgres.
```shell
docker run -d -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=db --network bot_random -p 5432:5432 --name  Postgres postgres:14
```
### Переходим в созданную нами БД Postgres.
```shell
docker exec -it Postgres psql --username admin --dbname db
```
### Создаем необходимую таблицу с данными, откуда бот будет брать информацию.
```shell
create table coin_random (
Eagle INT not null,
Tails INT not null);

insert into coin_random values (1,1);
```
### Собираем образ с помощью файлов из репозитория.
```shell
docker build -t bot_random:prod .
```
### Поднимаем бекенд, указывая токен бота.
```shell
docker run -d --name bot -e HOST=Postgres -e TOKEN="Передаем токен Телеграм бота" --network bot_random bot_random:prod
```
## Переходим в бота и проверяем его работу.

<a href="https://ibb.co/nfbq8yC"><img src="https://i.ibb.co/J2KWFTQ/IMG-20240512-203045.jpg" alt="IMG-20240512-203045" border="0" width="300" height="600" /></a>
