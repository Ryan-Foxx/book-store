import os
import uuid


def author_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"authors/avatars/{uuid.uuid4().hex}{ext}"
