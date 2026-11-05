import pytest
from apps.users.models import UserProfile


@pytest.mark.django_db
class TestUserProfileModel:

    def test_profile_str_representation(self, customer_user):
        # Verify string representation of UserProfile instance
        profile, _ = UserProfile.objects.get_or_create(user=customer_user)
        assert str(profile) == f"{customer_user} Profile"

    def test_user_profile_one_to_one_relation(self, customer_user):
        # Verify bidirectional OneToOne relationship between User and UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=customer_user)
        assert profile.user == customer_user
        assert customer_user.profile == profile
