# tg_bot_and_fastapi

Проект, объединяющий Telegram‑бота и FastAPI, который позволяет:

- Предоставить REST API для **постов** (создание, чтение, обновление, удаление) с Swagger UI  
- Запустить Telegram‑бота, который:  
  1. По командеPI для **пвыводит inline‑кнопки со всеми заголовками постов  
  2. При нажатии на кнопку шлёт полный текст поста (заголовок, дату создания, содержимое)

Вся работа с базой выполняется асинхронно через SQLAlchemy 2.0+ и миграции Alembic (по умолчанию SQLite).


## 🗂 Структура проекта

.
├── main.py             # точка входа: поднимает FastAPI и запускает бота
├── database.py         # асинхронный движок SQLAlchemy и фабрика сессий
├── crud.py             # функции CRUD для модели Post
├── posts/
│   ├── models.py       # ORM‑модель Post
│   ├── schemas.py      # Pydantic‑схемы для Post (создание/обновление)
│   └── router.py       # маршруты FastAPI под префиксом /posts
├── users/              # (опционально) логика аутентификации
├── migration/          # папка с миграциями Alembic
│   └── versions/
│       └── …         # файлы ревизий
├── database3.db        # пример файла SQLite (можно удалить)
├── requirements.txt    # список зависимостей
└── alembic.ini         # конфигурация Alembic


## 🚀 Быстрый старт

### 1. Клонировать и установить

```bash
git clone https://github.com/MashibaRyo/tg_bot_and_fastapi.git
cd tg_bot_and_fastapi
python -m venv .venv
source .venv/bin/activate            # macOS/Linux
# .venv\Scripts\activate             # Windows
pip install -r requirements.txt

2. Конфигурация

Создайте файл .env или экспортируйте переменные окружения:

export BOT_TOKEN="ваш_токен_бота"
export DATABASE_URL="sqlite+aiosqlite:///./database3.db"

Для PostgreSQL можно указать
export DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/dbname"

3. Применить миграции Alembic

alembic upgrade head

Это создаст таблицу posts в базе.

4. Запустить приложение

python main.py

 • FastAPI будет доступен по адресу http://127.0.0.1:8000
 • Swagger UI → http://127.0.0.1:8000/docs
 • Telegram‑бот начнёт polling


📦 REST API (FastAPI)

Все эндпойнты находятся под префиксом /posts.

Метод Путь Описание
GET /posts/ Получить список всех постов
GET /posts/{id} Получить пост по ID
POST /posts/ Создать новый пост
PATCH /posts/{id} Частично обновить поля поста
DELETE /posts/{id} Удалить пост

Попробовать их можно в Swagger UI: http://127.0.0.1:8000/docs.


🤖 Telegram‑бот

Команды
 • /posts
Бот присылает inline‑кнопки со всеми заголовками постов.
При нажатии на кнопку отправляет полный текст выбранного поста.

Как это работает
 1. В main.py настраиваются хендлеры aiogram:
 • /posts — запрос в БД, построение кнопок
 • callback_query — загрузка выбранного поста и отправка его текстом
 2. Для взаимодействия с Telegram используется aiogram.


⚙️ Настройки

Переменная Описание
BOT_TOKEN Токен вашего Telegram‑бота
DATABASE_URL URL подключения SQLAlchemy (SQLite и т.д.)

Переменные можно задавать в окружении или в файле .env (с помощью python-dotenv).


🛠️ Миграции Alembic
 • Сгенерировать новую миграцию после изменений в моделях:

alembic revision --autogenerate -m "описание изменений"


 • Применить миграции:

alembic upgrade head


 • Сбросить миграции (только для разработки):

rm migration/versions/*.py
alembic stamp head
alembic revision --autogenerate -m "baseline"
alembic upgrade head



✨ Contributing
 1. Форкните репозиторий
 2. Создайте ветку для фичи: git checkout -b feat/XYZ
 3. Внесите изменения и закоммитьте: git commit -m "Add XYZ"
 4. Запушьте в свой форк: git push origin feat/XYZ
 5. Откройте Pull Request
