from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.books'

    def ready(self):
        import apps.books.signals.author_avatar
        import apps.books.signals.translator_avatar
        import apps.books.signals.publisher_avatar
        import apps.books.signals.book_avatar
