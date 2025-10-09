# Book Store 📚

Hello everyone 👋

This is a **back-end bookstore project** inspired by the [**Fidibo**](https://fidibo.com) platform.  
It is **developed using the Django framework**, and more details are provided below.

## Tech Stack ⚙️

| Technology            | Version | Link                                                                                                                                           |
| --------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Python                | 3.13.5  | [![Python](https://img.shields.io/badge/Python-023047?logo=python)](https://www.python.org/downloads/release/python-3135/)                     |
| Django                | 5.2.6   | [![Django](https://img.shields.io/badge/Django-green?logo=django)](https://www.djangoproject.com/download/)                                    |
| MySql                 | 9.3.0   | [![MySql](https://img.shields.io/badge/MySql-023047?logo=mysql)](https://dev.mysql.com/downloads/mysql/)                                       |
| Django REST Framework | 3.16.1  | [![DRF](https://img.shields.io/badge/DRF-ff1709?logo=django)](https://www.django-rest-framework.org/#installation)                             |
| DRF Nested Routers    | 0.95.0  | [![DRF Nested Routers](https://img.shields.io/badge/DRF_Nested_Routers-green)](https://github.com/alanjds/drf-nested-routers)                  |
| Django Debug Toolbar  | 6.0.0   | [![Debug Toolbar](https://img.shields.io/badge/Debug_Toolbar-669bbc)](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) |
| Environs              | 14.3.0  | [![Environs](https://img.shields.io/badge/Environs-caf0f8)](https://github.com/sloria/environs)                                                |
| MySQLclient           | 2.2.7   | [![MySQLclient](https://img.shields.io/badge/MySQLclient-023047?logo=mysql)](https://github.com/PyMySQL/mysqlclient)                           |
| Uv                    | 0.8.15  | [![Uv](https://img.shields.io/badge/Uv-blue?logo=uv)](https://docs.astral.sh/uv/getting-started/installation/)                                 |

## Features ✨

-   [x] Basic Django project setup
-   [ ] RESTful API for book data
-   [ ] Admin dashboard
-   [ ] User authentication and authorization
-   [ ] Search and filtering system

_(You can expand this list as the project grows.)_

## Installation 🔧

1. Clone the repository:

```bash
git clone https://github.com/Ryan-Foxx/book-store.git

cd book-store

create a database called [book_store] in mysql
```

2. Create a **.env** file in the **root directory** and add the following variables:

```bash
# DJANGO_SECRET_KEY must be a 66-character, complex text.
DJANGO_SECRET_KEY=Django-Secret-Key
DJANGO_DEBUG=True
DB_NAME=book_store
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```

3. Create and activate a virtual environment:

```bash
# Create virtual environment with → pip
python -m venv venv

# Create virtual environment with → uv
uv venv

# Activate virtual environment → Linux/Mac
source venv/bin/activate

# Activate virtual environment → Windows
venv\Scripts\activate
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

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

---
