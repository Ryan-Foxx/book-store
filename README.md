# Bookstore 📚

Hello everyone 👋

This is a **bookstore project** inspired by the [**Fidibo**](https://fidibo.com) platform.  
It is **developed using the Django framework**, and more details are provided below.

## Tech Stack ⚙️

> [!IMPORTANT]  
> These versions of the technologies were available at the time the project was created, but if you have a higher version, there is no need to worry.

### Docker Desktop v4.85.0:

<img src="https://skillicons.dev/icons?i=docker" height="60" alt="docker logo"  />

### `Backend:`

| Technology            | Version | Link                                                                                                                                           |
| --------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Python                | 3.12.3  | [![Python](https://img.shields.io/badge/Python-023047?logo=python)](https://www.python.org/)                                                   |
| Django                | 5.2.11  | [![Django](https://img.shields.io/badge/Django-green?logo=django)](https://www.djangoproject.com/download/)                                    |
| Django REST Framework | 3.16.1  | [![DRF](https://img.shields.io/badge/DRF-ff1709?logo=django)](https://www.django-rest-framework.org/#installation)                             |
| Django Debug Toolbar  | 6.1.0   | [![Debug Toolbar](https://img.shields.io/badge/Debug_Toolbar-669bbc)](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) |
| Uv                    | 0.11.17 | [![Uv](https://img.shields.io/badge/Uv-blue?logo=uv)](https://docs.astral.sh/uv/getting-started/installation/)                                 |

### `Frontend:` None

<!-- | Technology  | Version | Link                                                                                                             |
| ----------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| Nextjs      | 16.1.6  | [![Nextjs](https://img.shields.io/badge/Nextjs-242938?logo=next.js)](https://nextjs.org/)                        |
| React       | 19.2.4  | [![React](https://img.shields.io/badge/React-blue?logo=react)](https://react.dev/)                               |
| TypeScript  | 5.9.3   | [![TypeScript](https://img.shields.io/badge/TypeScript-1d3557?logo=typescript)](https://www.typescriptlang.org/) |
| Tailwindcss | 4.1.17  | [![Tailwindcss](https://img.shields.io/badge/Tailwindcss-023e8a?logo=tailwindcss)](https://tailwindcss.com/)     | -->

### `Database:`

| Technology | Version | Link                                                                                                     |
| ---------- | ------- | -------------------------------------------------------------------------------------------------------- |
| Postgres   | 18.1    | [![Postgres](https://img.shields.io/badge/Postgres-242938?logo=postgresql)](https://www.postgresql.org/) |

---

## Features ✨

- [x] Basic Django project setup
- [x] RESTful API for book data
- [x] Search and filtering system
- [x] Admin dashboard
- [x] User authentication and authorization

`_(You can expand this list as the project grows.)_`

## Installation 🔧

1. Clone the repository:

```bash
git clone https://github.com/Ryan-Foxx/book-store.git

cd book-store
```

2. Create two `.env` files in the `root directory` named `.env.backend.dev` and `.env.compose.dev` and add the following variables to them:

##### `.env.backend.dev:`

```bash
# [DJANGO_SECRET_KEY] and [JWT_SIGNING_KEY] must be a 66-character, complex text.

SECRET_KEY=6^z3*&w_u_z@+v^jwfn-rjmvqz!&$j5uth*9gial8yv+lxx7t1
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=True

# REST_FRAMEWORK THROTTLE
ANON_RATE_THROTTLE=1000/hour
USER_RATE_THROTTLE=1000/day
REGISTER_RATE_THROTTLE=1000/hour
LOGIN_RATE_THROTTLE=1000/min
ACTIVATION_RATE_THROTTLE=1000/min
RESEND_ACTIVATION_RATE_THROTTLE=1000/hour
RESET_PASSWORD_RATE_THROTTLE=1000/hour
RESET_PASSWORD_CONFIRM_RATE_THROTTLE=1000/min
RESET_USERNAME_RATE_THROTTLE=1000/hour
SET_PASSWORD_RATE_THROTTLE=1000/min
SET_USERNAME_RATE_THROTTLE=1000/min

# Djoser
DJOSER_LOGIN_FIELD=username
DJOSER_SEND_ACTIVATION_EMAIL=True
DJOSER_SEND_CONFIRMATION_EMAIL=True
SEND_USERNAME_RESET_EMAIL=True
DJOSER_PASSWORD_RESET_CONFIRM_URL=reset-password/{uid}/{token}
DJOSER_USERNAME_RESET_CONFIRM_URL=reset-username/{uid}/{token}
DJOSER_ACTIVATION_URL=activate/{uid}/{token}

# SIMPLE JWT
JWT_ACCESS_TOKEN_MINUTES=1440
JWT_REFRESH_TOKEN_DAYS=1
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
JWT_AUTH_HEADER_TYPE=Bearer
JWT_SIGNING_KEY=s#a0%5d_l2rop!$jt4r(xaixunigse%0u$l&c9y9wty0fqaa%w
JWT_ALGORITHM=HS256
JWT_UPDATE_LAST_LOGIN=True

# For Development: Mailhog Email System
EMAIL_HOST=mailhog
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=noreply@bookstore.local
```

##### `.env.compose.dev:`

```bash

# To connect to the database
POSTGRES_DB=book_store_dev_db
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# URL for the database
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Database Port
DATABASE_PORT=5432

# Backend Port
BACKEND_PORT=8000

# Mailhog Port
MAILHOG_SMTP_PORT=1025
MAILHOG_UI_PORT=8025
```

3. Create and activate a virtual environment:

```bash
# Create virtual environment with → pip
python -m venv venv

# Create virtual environment with → uv
uv venv

# Activate virtual environment → Linux/Mac
source .venv/bin/activate

# Activate virtual environment → Windows
.\venv\Scripts\activate
```

4. Install dependencies:

```bash
# Install dependencies with → pip
pip install -r requirements.txt

# Install dependencies with → uv
uv pip install -r requirements.txt

# Installing dependencies based on pyproject.toml → uv
uv sync
```

5. Start Project:

```bash
docker-compose -f docker-compose.dev.yml --env-file .env.compose.dev up --build
```

6. Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

---
