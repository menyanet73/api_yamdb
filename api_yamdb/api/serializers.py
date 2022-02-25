from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews import models


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=models.Genre.objects.all())]
    )

    class Meta:
        model = models.Genre
        exclude = ['id', ]
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=models.Category.objects.all())]
    )

    class Meta:
        model = models.Category
        exclude = ['id', ]
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=models.Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=models.Category.objects.all())

    class Meta:
        model = models.Title
        fields = '__all__'

    def validate_year(self, year):
        if year > timezone.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не созданы.'
            )
        return year


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = models.Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Review
        exclude = ['title', ]

    def validate(self, data):
        if self.context['view'].action == 'create':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if models.Review.objects.filter(
                    title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Уже есть отзыв от этого пользователя на этот фильм')
        return data

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
        model = models.Comment
        exclude = ['review', ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        lookup_field = 'username'
        validators = [
            UniqueTogetherValidator(
                queryset=models.User.objects.all(),
                fields=['username', 'email']
            )
        ]
        read_only_fields = ('role',)

    def validate_email(self, email):
        if self.context['view'].action == 'create':
            if models.User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует')
        return email


class SignUpUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.User.objects.all())])

    class Meta:
        model = models.User
        fields = ('username', 'email')

    def validate_username(self, username):
        if self.context.get('username') == username:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует')
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username me')
        return username


class TokenCreateSerializer(serializers.ModelSerializer):
    queryset = models.User.objects.all()

    class Meta:
        model = models.User
        fields = ('username', 'confirmation_code')


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = 'username'
        validators = [
            UniqueTogetherValidator(
                queryset=models.User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_email(self, email):
        if self.context['view'].action == 'create':
            if models.User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует')
        return email
