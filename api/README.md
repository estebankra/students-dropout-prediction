## Requirements

- Python 3.10

## .env

### Generate SECRET_KEY

```shell
openssl rand -hex 32
```

## Install postgres

https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart

## Setup

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install -r requirements.txt
```
### DB Migrations
```shell
alembic upgrade head
```
## Run

```shell
ENVIRONMENT=development uvicorn app.main:app --reload --timeout-keep-alive 30
```

## Environments

```shell
ENVIRONMENT=development|testing|production
```

## Run tests

```shell
pytest
```

## Create new db migrations
```shell
alembic revision --autogenerate -m "name"
```