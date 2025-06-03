# Battleship API

API для игры "Морской бой" с использованием FastAPI, sqlalchemy, PostgreSQL.

---

## Запуск

Для запуска требуется установленный Docker и Docker Compose.

Команда для запуска сервиса:

```bash
docker-compose up --build
```

---

## Проверка

В репозитории есть postman коллекция: postman-collection.json
Для проверки ws:
```
ws://localhost:8000/games/{{game_sid}}/play?player_sid={{player_sid}}
```
body для сообщений в ws:
```
{
"type": "move",
"x": 3,
"y": 5
}
```