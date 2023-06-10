![vereb01/yamdb_final](https://github.com/vereb01/yamdb_final-1/actions/workflows/yamdb_workflow.yml/badge.svg) # сделать значек нового проекта 

Проект доступен по адресу 


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
  cd backend\foodgram
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
Для размещения проекта вам наподобиться сервер, например ВМ Yandex.Cloud. Далее нам необходимо установить Docker и docker-compose на сервер:

# username - ваш логин, ip - ip виртуальной машины
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo systemctl start docker.service && sudo systemctl enable docker.service
С установкой закончили!

Разворачиваем проект:
Предварительно из папки /backend и /frontend загрузим актуальные данные на DockerHub (на вашем ПК):

sudo docker login -u <ваше имя пользователя на DockerHub>
cd backend
sudo docker build -t <ваше имя пользователя на DockerHub>/foodgram_backend:latest .
sudo docker push <ваше имя пользователя на DockerHub>/foodgram_backend:latest
cd ..
cd frontend
sudo docker build -t <ваше имя пользователя на DockerHub>/foodgram_frontend:latest .
sudo docker push <ваше имя пользователя на DockerHub>/foodgram_frontend:latest
Перенесите файлы docker-compose.yml и nginx.conf на сервер, из папки infra в текущем репозитории (на вашем ПК).

cd infra
scp docker-compose.yml username@server_ip:/home/username/
scp nginx.conf username@server_ip:/home/username/
Так же, создаем файл .env в директории infra на ВМ:

touch .env
Заполнить в настройках репозитория секреты .env

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=ultra_mega_key5%78@gsltmb
Всё готово! Далее в папке infra выполняем команду:

sudo docker-compose up -d --build
Проект запустится на ВМ и будет доступен по указанному вами адресу либо IP. Нужно завершить настройку на ВМ:

В папке infra выполняем команду, что бы собрать контейнеры:
Остановить:

sudo docker-compose stop
Удалить вместе с volumes:

# Осторожно, команда удаляет данные!
sudo docker-compose down -v
Для доступа к контейнеру backend и сборки финальной части выполняем следующие команды:

sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
Дополнительно можно наполнить ваше базу ингредиентами:

sudo docker-compose exec backend python manage.py load_ingredients
Всё! Ваш продуктовый помощник запущен, можно наполнять его рецептами и делится с друзьями!

Запуск проекта в Docker на localhost
Для Linux ставим Docker как описано выше, для Windows устанавливаем актуальный Docker Desktop.

В папке infra выполняем команду, что бы собрать контейнеры:

sudo docker-compose up -d --build
Остановить:

sudo docker-compose stop
Удалить вместе с volumes:

# Осторожно, команда удаляет данные!
sudo docker-compose down -v
Для доступа к контейнеру выполняем следующие команды:

sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
Дополнительно можно наполнить DB ингредиентами и тэгами:

sudo docker-compose exec backend python manage.py load_tags
sudo docker-compose exec backend python manage.py load_ingredients
Если вам необходимо создать базу и пользователя в PostgreSql (если будет необходимость запустить проект без Docker):

sudo -u postgres psql
CREATE DATABASE basename;
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE basename TO username;
Документация к API доступна после запуска
http://127.0.0.1/api/docs/
