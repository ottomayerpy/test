# anothertest

## Инициализация
```
git clone https://github.com/ottomayerpy/test
cd another_test
nano .env
docker-compose up
```

В .env кладем следующее:
```
  POSTGRES_USER=postgres
  POSTGRES_NAME=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  PGDATA=/var/lib/postgresql/data/pgdata
```

Супер пользователь - admin:admin
