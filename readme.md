auth_service/
│
├── alembic/                  # Миграции
├── app/
│   ├── api/                  # Роуты (в т.ч. google_auth)
│   ├── core/                 # Настройки, email, JWT и т.д.
│   ├── models/               # SQLAlchemy-модели
│   ├── schemas/              # Pydantic-схемы
│   ├── services/             # Бизнес-логика
│   ├── utils/                # Вспомогательные функции
│   └── main.py               # FastAPI-приложение
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

........................................................................................
✅ Цель:
Реализовать авторизацию через Google OAuth2.

Если пользователь с таким email не найден — автоматически создать его.

Всё в стиле LAF_microcervices: структура, стили, зависимости, .env и pydantic-settings.

Используем authlib для OAuth2.

📁 Структура, которую создадим:
pgsql
Копировать
Редактировать
auth_service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── google_auth.py  # эндпоинт /auth/google
│   ├── core/
│   │   ├── config.py                # pydantic-settings
│   │   └── security.py              # логика OAuth2
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   ├── crud/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── main.py
├── .env