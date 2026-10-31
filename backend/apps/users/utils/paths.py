import os
import uuid

def user_profile_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"users/users-profiles/avatars/{uuid.uuid4().hex}{ext}"
