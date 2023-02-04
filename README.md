# anothertest

## Инициализация
```
git clone https://github.com/ottomayerpy/test
cd test/another_test
nano .env
cd ..
docker-compose up
```
Сервер доступен по адресу localhost:8000

В .env кладем следующее:
```
  POSTGRES_USER=postgres
  POSTGRES_NAME=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  PGDATA=/var/lib/postgresql/data/pgdata
  PAYOUT_AMOUNT=50
```

Супер пользователь - admin:admin

* Приложение разрабатывалось и тестировалось в Linux Mint 20.3 Cinnamon 5.2.7 (6.0.9-060009-generic)

* nano - встроенный в mint консольный текстовый редактор
