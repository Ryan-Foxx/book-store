from apps.books.models import Translator
from rest_framework import serializers


class TranslatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ("id", "name", "avatar")


class TranslatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = ("id", "name", "avatar", "about")
