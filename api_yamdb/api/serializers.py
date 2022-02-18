from datetime import datetime
from rest_framework import serializers

from reviews.models import Title, Genre, Category, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True, required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        queryset = obj.reviews.all()
        rates = 0
        for query in queryset:
            rates += int(query.score)
        if rates == 0:
            return 0
        return round(rates / len(queryset))

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
        fields = '__all__'
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.RegexField(regex='^[-a-zA-Z0-9_]+$')

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate_score(self, score):
        if 1 >= score >= 10:
            return score
        raise serializers.ValidationError(
            "Оценка может быть только целым числом от 1 до 10")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
