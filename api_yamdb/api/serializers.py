from datetime import datetime
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Genre, Category, Review, Comment, User


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()

    class Meta:
        model = Genre
        fields = ['name', 'slug']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ['name', 'slug']
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, year):
        if year > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не созданы.'
            )
        return year

class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        queryset = obj.reviews.all()
        rates = None
        if queryset:
            rates = 0
        for query in queryset:
            rates += int(query.score)
        if rates is None:
            return None
        return round(rates / len(queryset))


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate_score(self, score):
        if 1 <= score <= 10:
            return score
        raise serializers.ValidationError(
            'Оценка может быть только целым числом от 1 до 10')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class SignUpUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if self.context.get("username") == username:
            raise serializers.ValidationError("You can't create exist user.")
        return username


class TokenCreateSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(source='password', required=True)

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')
