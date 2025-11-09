# incident-scrapper

API carrying incidents from txt chats

## Стек

- Python 3.14
- Основная связка: FastAPI + Postgres 15

В качестве ORM выбрана SQLAlchemy, используется docker для контейнеризации, внутри которого пашет под uvicorn.

## Структура проекта

```md
.
├── app
│   ├── api
│   │   ├── __init__.py
│   │   └── incident.py  
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── middleware.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── incident.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── incident.py
│   └── services
│       ├── __init__.py
│       └── incident_service.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

> Каждый каталог, соответственно, разделяет ответственность между -py модулями; утилиты, конфигурации, эндпоинты, обработка запросов, модели БД и схемы валидации.

## Fast start

На машине должен быть **Docker** и, соответственно, **docker-compose**

Я спрятал креды для базы данных в .env файле; структура его в точности такая же, как в .env.mock;
**Его необходимо создать и заполнить.**

docker-compose.yml сделан так, что сам поднимает контейнер с базой данных, поэтому этот шаг
можно считать условным, но база данных не поднимется без этих переменных в окружении.

Для запуска достаточно выполнить в терминале:

```sh
git clone https://github.com/ex8ed/incident-scrapper.git
cd incident-scrapper

docker-compose up --build
```

Приложение будет доступно на http://localhost:8000

> Swagger: http://localhost:8000/docs

## Статусы и источники

Статусы и источники представляют собой конечные наборы значений с проверкой (при указании иного возврат 422):

Статусы:

- open
- in_process
- resolved
- closed

Источники инцидентов:

- operator
- monitoring
- partner

## Эндпоинты

### Cоздание запроса (POST), /incidents/

> Принимает два поля в теле, description и source.

### Получение списка инцидентов (GET) /incidents/

> Реализован с фильрацией по статусу и лимитом; query-параметры.

### Обновление статуса (PATCH) /incidents/{id}

> id – path-параметр; при отсутствии подходящего id вернет 404

Более подробная документация доступна в swagger, или в [openapi.json](https://github.com/ex8ed/incident-master/blob/main/openapi.json)
