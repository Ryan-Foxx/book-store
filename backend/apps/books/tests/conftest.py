import pytest
from apps.books.models import Author, Award
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
