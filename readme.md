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