import pytest
from apps.users.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction


# Enable real database transactions so that transaction.on_commit hooks are executed
@pytest.mark.django_db(transaction=True)
class TestUserProfileSignals:

    def test_old_avatar_cleaned_up_on_replacement(self, user_factory):
        # Create a user and their profile with an initial avatar
        user = user_factory(username="avatartest1", email="avatar1@example.com")
        profile = user.profile

        # Create dummy image files for upload
        avatar1_file = SimpleUploadedFile("avatar1.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")
        avatar2_file = SimpleUploadedFile("avatar2.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")

        # Set and save the first avatar
        profile.avatar.save("avatar1.jpg", avatar1_file, save=True)
        avatar1_name = profile.avatar.name

        # Verify storage exists for the first avatar
        assert profile.avatar.storage.exists(avatar1_name)

        # Replace the avatar with a new one
        profile.avatar.save("avatar2.jpg", avatar2_file, save=True)
        avatar2_name = profile.avatar.name

        # Verify the new avatar exists and the old avatar has been deleted from storage
        assert profile.avatar.storage.exists(avatar2_name)
        assert not profile.avatar.storage.exists(avatar1_name)

    def test_avatar_deleted_on_profile_deletion(self, user_factory):
        # Create a user and profile with an avatar
        user = user_factory(username="avatartest2", email="avatar2@example.com")
        profile = user.profile

        avatar_file = SimpleUploadedFile("avatar_del.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")
        profile.avatar.save("avatar_del.jpg", avatar_file, save=True)
        avatar_name = profile.avatar.name

        # Verify avatar file exists in storage
        assert profile.avatar.storage.exists(avatar_name)

        # Delete the user profile inside an atomic block
        with transaction.atomic():
            profile.delete()

        # Verify that the avatar file is removed from storage upon deletion commit
        # Since profile storage might use default storage backend
        from django.core.files.storage import default_storage

        assert not default_storage.exists(avatar_name)
