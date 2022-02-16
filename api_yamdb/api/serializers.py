from datetime import datetime
from rest_framework import serializers

from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, year):
        if year > datetime.year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения, которые еще не созданы."
                )


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(regex='^[-a-zA-Z0-9_]+$')

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(regex='^[-a-zA-Z0-9_]+$')
    
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
