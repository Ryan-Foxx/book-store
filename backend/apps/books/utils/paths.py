import os
import uuid


def author_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"authors/avatars/{uuid.uuid4().hex}{ext}"


def translator_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"books/translators/avatars/{uuid.uuid4().hex}{ext}"


def publisher_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"books/publishers/avatars/{uuid.uuid4().hex}{ext}"


def book_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"books/books/avatars/{uuid.uuid4().hex}{ext}"
