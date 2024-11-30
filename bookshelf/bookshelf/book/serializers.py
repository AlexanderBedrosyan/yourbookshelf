from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_full_name', 'description', 'genre']

    def get_author_full_name(self, obj):
        return obj.author.get_full_name()

