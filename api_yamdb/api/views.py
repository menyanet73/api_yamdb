from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews import models

from api import serializers
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorOrAdminOrReadOnly)

from .filters import TitleFilter
from .viewsets import CreateDeleteListViewset


class GenreViewSet(CreateDeleteListViewset):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateDeleteListViewset):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.TitleGetSerializer
        else:
            return serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = models.Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        current_title = get_object_or_404(models.Title, pk=title_id)
        current_user = self.request.user
        serializer.save(title=current_title, author=current_user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = models.Comment.objects.filter(review=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        current_review = get_object_or_404(models.Review, pk=review_id)
        current_user = self.request.user
        serializer.save(review=current_review, author=current_user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if (self.request.user.role in ['admin']
                or self.request.user.is_superuser):
            return serializers.AdminSerializer
        else:
            return serializers.UserSerializer

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = serializers.UserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SignUpUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.SignUpUserSerializer(data=request.data)
        registration_username = request.data.get('username')
        registrstion_email = request.data.get('email')
        if registration_username == 'me':
            raise exceptions.ValidationError
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            user = models.User.objects.get(username=registration_username)
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Код подтверждения регистрации.',
                message=f'Ваш код для регистрации: {confirmation_code}',
                from_email='test@mail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(
                {
                    'email': registrstion_email,
                    'username': registration_username
                },
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenCreateSerializer(data=request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError(serializer.errors)
        user = get_object_or_404(
            models.User, username=self.request.data['username'])
        if request.data['confirmation_code'] != user.confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )
