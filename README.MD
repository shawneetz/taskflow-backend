TaskFlow Project
5.1 Project Structure
backend/
├── app/
│ ├── **init**.py
│ ├── main.py # FastAPI app factory, middleware, routers
│ ├── config.py # pydantic-settings BaseSettings
│ ├── dependencies.py # Shared FastAPI dependencies (get_db, get_current_user)
│ │
│ ├── db/
│ │ ├── **init**.py
│ │ ├── base.py # SQLAlchemy DeclarativeBase
│ │ └── session.py # Async engine + session factory
│ │
│ ├── models/
│ │ ├── **init**.py
│ │ ├── user.py
│ │ ├── task.py
│ │ └── tag.py
│ │
│ ├── schemas/
│ │ ├── **init**.py
│ │ ├── auth.py # TokenResponse, LoginRequest
│ │ ├── user.py # UserCreate, UserRead, UserUpdate
│ │ ├── task.py # TaskCreate, TaskRead, TaskUpdate, TaskReorder
│ │ └── tag.py # TagCreate, TagRead, TagUpdate
│ │
│ ├── routers/
│ │ ├── **init**.py
│ │ ├── auth.py
│ │ ├── users.py
│ │ ├── tasks.py
│ │ └── tags.py
│ │
│ ├── services/
│ │ ├── **init**.py
│ │ ├── auth_service.py # Token creation, verification, refresh logic
│ │ ├── task_service.py # Business logic for task operations
│ │ └── tag_service.py # Business logic for tag operations
│ │
│ └── core/
│ ├── **init**.py
│ ├── security.py # Password hash, JWT encode/decode
│ └── exceptions.py # Custom HTTP exceptions
│
├── alembic/
│ ├── env.py
│ ├── script.py.mako
│ └── versions/ # Migration files
│
├── tests/
│ ├── conftest.py # Fixtures: test DB, test client, test user
│ ├── test_auth.py
│ ├── test_tasks.py
│ └── test_tags.py
│
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml # Dependencies via uv
├── .env.example
└── README.md
