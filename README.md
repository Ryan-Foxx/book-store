# Book Store 📚

Hello everyone 👋

This is a **back-end bookstore project** inspired by the [**Fidibo**](https://fidibo.com) platform.  
It is **developed using the Django framework**, and more details are provided below.


## Tech Stack ⚙️

| Technology | Version | Badge |
|------------|---------|-------|
| Python     | 3.13.5    | [![Python](https://img.shields.io/badge/Python-3.13.5-blue?logo=python)](https://www.python.org/downloads/release/python-3135/) |
| Django     | 5.2.6   | [![Django](https://img.shields.io/badge/Django-5.2.6-green?logo=django)](https://www.djangoproject.com/download/) |

## Features ✨
- [ ]  Basic Django project setup
- [ ]  RESTful API for book data
- [ ]  Admin dashboard
- [ ]  User authentication and authorization
- [ ]  Search and filtering system

*(You can expand this list as the project grows.)*


## Installation 🔧
1. Clone the repository:
   ```bash
   git clone https://github.com/Ryan-Foxx/book-store.git

   cd book-store
2. Create and activate a virtual environment:
    ```bash
    # Create virtual environment with → pip
    python -m venv venv

    # Create virtual environment with → uv
    uv venv

    # Activate virtual environment → Linux/Mac
    source venv/bin/activate

    # Activate virtual environment → Windows
    venv\Scripts\activate
3. Install dependencies:
    ```bash
    # Install dependencies with → pip
    pip install -r requirements.txt
    
    # Install dependencies with → uv
    uv pip install -r requirements.txt

    # Installing dependencies based on pyproject.toml → uv
    uv sync
4. Start the development server:
    ```bash
    python manage.py runserver
---
