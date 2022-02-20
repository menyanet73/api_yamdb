from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Genre, Category, Review, Comment, User


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', 'rating')

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
                'Нельзя добавлять произведения, которые еще не созданы.'
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

    def validate_score(self, score):
        if 1 >= score >= 10:
            return score
        raise serializers.ValidationError(
            'Оценка может быть только целым числом от 1 до 10')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


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
