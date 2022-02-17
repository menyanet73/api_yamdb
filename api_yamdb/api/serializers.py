from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Title, Genre, Category, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', 'rating')

    def get_rating(self, obj):
        queryset = obj.reviews.all()
        rates = []
        for query in queryset:
            rates.append(int(query.score))
        if len(rates) == 0:
            return 0
        return round(sum(rates)/len(rates))

    def validate_year(self, year):
        if year > datetime.now().year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения, которые еще не созданы."
                )
        return year


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'