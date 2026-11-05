import pytest
from apps.users.models import User, UserProfile
from rest_framework.test import APIClient


@pytest.fixture
def user_password():
    return "testpass123"


@pytest.fixture
def user_factory(db, user_password):
    counter = {"value": 0}

    def create_user(**kwargs):
        counter["value"] += 1
        index = counter["value"]

        defaults = {
            "username": f"testuser{index}",
            "email": f"testuser{index}@example.com",
            "phone_number": f"0912000{index:04d}",
            "password": user_password,
            "role": User.ROLE_CHOICE_CUSTOMER,
        }
        defaults.update(kwargs)
        # Use create_user to enforce password hashing and manager validations
        return User.objects.create_user(**defaults)

    return create_user


@pytest.fixture
def user_profile_factory(db, user_factory):
    def create_user_profile(user=None, **kwargs):
        # Fall back to creating a new user if none is provided
        if user is None:
            user = user_factory()

        # The post_save signal automatically provisions UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Apply any optional attribute updates (e.g. avatar)
        if kwargs:
            for attr, val in kwargs.items():
                setattr(profile, attr, val)
            profile.save()

        return profile

    return create_user_profile


@pytest.fixture
def owner_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_OWNER)


@pytest.fixture
def admin_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_ADMIN)


@pytest.fixture
def customer_user(user_factory):
    return user_factory(role=User.ROLE_CHOICE_CUSTOMER)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)
    return api_client
