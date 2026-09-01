import datetime

import pytest
from apps.books.models import (
    Author,
    Award,
    Book,
    Category,
    Language,
    Publisher,
    Translator,
)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


# =========== Factories ===========
@pytest.fixture
def user_factory(db):
    counter = {"value": 0}

    def create_user(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "username": f"user{index}",
            "email": f"user{index}@example.com",
            "phone_number": f"0912000{index:04d}",
            "password": "testpass123",
            "role": User.ROLE_CHOICE_CUSTOMER,
        }
        defaults.update(kwargs)

        return User.objects.create_user(**defaults)

    return create_user


@pytest.fixture
def author_factory(db):
    counter = {"value": 0}

    def create_author(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "name": f"Author {index}",
            "about": f"About Author {index}",
            "biography": f"Biography Author {index}",
            "avatar": None,
        }
        defaults.update(kwargs)

        return Author.objects.create(**defaults)

    return create_author


@pytest.fixture
def award_factory(db):
    counter = {"value": 0}

    def create_award(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "title": f"Award {index}",
            "year_received": None,
        }
        defaults.update(kwargs)

        return Award.objects.create(**defaults)

    return create_award


@pytest.fixture
def translator_factory(db):
    counter = {"value": 0}

    def create_translator(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "name": f"Translator {index}",
            "about": f"About Translator {index}",
            "avatar": None,
        }
        defaults.update(kwargs)

        return Translator.objects.create(**defaults)

    return create_translator


@pytest.fixture
def publisher_factory(db):
    counter = {"value": 0}

    def create_publisher(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "name": f"Publisher {index}",
            "about": f"About Publisher {index}",
            "avatar": None,
        }
        defaults.update(kwargs)

        return Publisher.objects.create(**defaults)

    return create_publisher


@pytest.fixture
def category_factory(db):
    counter = {"value": 0}

    def create_category(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "title": f"Category {index}",
            "description": f"Description for category {index}",
        }
        defaults.update(kwargs)

        return Category.objects.create(**defaults)

    return create_category


@pytest.fixture
def language_factory(db):
    counter = {"value": 0}

    def create_language(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "name": f"Language {index}",
        }
        defaults.update(kwargs)

        return Language.objects.create(**defaults)

    return create_language


@pytest.fixture
def book_factory(db, language_factory):
    counter = {"value": 0}

    def create_book(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        authors = kwargs.pop("authors", None)
        translators = kwargs.pop("translators", None)
        categories = kwargs.pop("category", None)

        if "language" not in kwargs:
            kwargs["language"] = language_factory()

        defaults = {
            "name": f"Book {index}",
            "price": 50000,
            "number_of_pages": 200,
            "publication_date": datetime.date(2025, 1, 1),
            "inventory": 10,
            "is_active": True,
            "avatar": None,
        }
        defaults.update(kwargs)

        book = Book.objects.create(**defaults)

        if authors is not None:
            book.authors.set(authors)
        if translators is not None:
            book.translators.set(translators)
        if categories is not None:
            book.category.set(categories)

        return book

    return create_book


# =========== Users ===========
@pytest.fixture
def owner_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_OWNER)


@pytest.fixture
def admin_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_ADMIN)


@pytest.fixture
def customer_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_CUSTOMER)


# =========== Clients ===========
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def owner_client(api_client, owner_user):
    api_client.force_authenticate(user=owner_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def customer_client(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)
    return api_client


# =========== Public Routes ===========
@pytest.fixture
def public_author_list_url():
    return reverse("public-author-list")


@pytest.fixture
def public_author_detail_url():
    def url(author_id):
        return reverse("public-author-detail", kwargs={"pk": author_id})

    return url


# =========== Admin Routes ===========
@pytest.fixture
def admin_author_list_url():
    return reverse("admin-author-list")


@pytest.fixture
def admin_author_detail_url():
    def url(author_id):
        return reverse("admin-author-detail", kwargs={"pk": author_id})

    return url


@pytest.fixture
def admin_award_list_url():
    return reverse("admin-award-list")


@pytest.fixture
def admin_award_detail_url():
    def url(award_id):
        return reverse("admin-award-detail", kwargs={"pk": award_id})

    return url
