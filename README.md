![vereb01/yamdb_final](https://github.com/vereb01/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Проект доступен по адресу [51.250.90.79](http://51.250.90.79/)


## foodgram-project-react
приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

Стек: Python 3.7, Django, DRF, Simple-JWT, PostgreSQL, Docker, nginx, gunicorn, GitHub Actions (CI/CD).

### Шаблон наполнения env-файла:
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres 
    DB_HOST=db
    DB_PORT=5432 

### Развертывание проекта:

Клонируем репозиторий к себе на ПК:

```bash
  git clone https://github.com/vereb01/foodgram-project-react.git
```

Переходим в дерикторию с проектом:

```bash
  cd foodgram
  cd backend/foodgram
```

Устанавливаем Виртуальное окружение:

```bash
  python -m venv venv
```

Активируем виртуальное окружение:

```bash
  source venv/Scripts/activate
```

Устанавливаем зависимости:

```bash
  pip install -r requirements.txt
```

Запуск с использованием CI/CD и Docker
Для успешного запуска вам надобиться добавить список Secrets в Settings -> Secrets and variables -> actions:
``` bash
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
PASSPHRASE
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY # здесь добавляется закрытый ключ. От строки "начало ключа" до "конец ключа" включительно cat ~/.ssh/id_rsa
TELEGRAM_TO
TELEGRAM_TOKEN
USER
```
В директории infra следует выполнить команды:
```
docker-compose up -d
docker-compose exec Django python manage.py makemigrations
docker-compose exec Django python manage.py migrate
docker-compose exec Django python manage.py collectstatic --no-input
```

