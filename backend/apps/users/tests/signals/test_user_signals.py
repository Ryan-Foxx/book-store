import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from apps.users.models import UserProfile

User = get_user_model()


# Enable real database transactions so that transaction.on_commit hooks are executed
@pytest.mark.django_db(transaction=True)
class TestUserSignals:

    def test_user_profile_is_created_automatically(self, user_factory):
        # Verify that creating a user automatically triggers the creation of a corresponding UserProfile
        user = user_factory(username="profiletest", email="profiletest@example.com")
        
        profile = UserProfile.objects.filter(user=user).first()
        assert profile is not None
        assert profile.user == user

    def test_token_revocation_on_password_change(self, customer_user):
        # Generate valid JWT tokens for the customer user
        refresh = RefreshToken.for_user(customer_user)
        refresh_token_str = str(refresh)
        
        # Ensure outstanding token exists and is not blacklisted initially
        assert OutstandingToken.objects.filter(token=refresh_token_str).exists()
        assert not BlacklistedToken.objects.filter(token__token=refresh_token_str).exists()

        # Change user's password which triggers token revocation on commit
        customer_user.set_password("newsecretpassword456")
        customer_user.save()

        # Verify that the refresh token was blacklisted by the post_save on_commit hook
        assert BlacklistedToken.objects.filter(token__token=refresh_token_str).exists()

    def test_token_revocation_on_role_change(self, customer_user):
        # Generate valid JWT tokens for the customer user
        refresh = RefreshToken.for_user(customer_user)
        refresh_token_str = str(refresh)

        # Update user role to admin (critical security change)
        customer_user.role = User.ROLE_CHOICE_ADMIN
        customer_user.save()

        # Verify that tokens are blacklisted due to role elevation/change
        assert BlacklistedToken.objects.filter(token__token=refresh_token_str).exists()

    def test_token_revocation_on_deactivation(self, customer_user):
        # Generate valid JWT tokens for the customer user
        refresh = RefreshToken.for_user(customer_user)
        refresh_token_str = str(refresh)

        # Deactivate the user
        customer_user.is_active = False
        customer_user.save()

        # Verify that tokens are blacklisted when the user is deactivated
        assert BlacklistedToken.objects.filter(token__token=refresh_token_str).exists()

    def test_no_token_revocation_on_non_security_field_update(self, customer_user):
        # Generate valid JWT tokens
        refresh = RefreshToken.for_user(customer_user)
        refresh_token_str = str(refresh)

        # Update a non-security field (e.g., username)
        customer_user.username = "updatedusername"
        customer_user.save()

        # Verify that tokens are NOT blacklisted for non-security updates
        assert not BlacklistedToken.objects.filter(token__token=refresh_token_str).exists()
