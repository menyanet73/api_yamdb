from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, status, exceptions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from api import serializers
from api.permissions import (
    IsAuthorOrAdminOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin)
from .viewsets import CreateDeleteListViewset, RetrievDeleteViewSet
from reviews.models import Title, Genre, Category, Review, Comment, User
from .filters import TitleFilter


class GenreViewSet(CreateDeleteListViewset):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(CreateDeleteListViewset):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
        queryset = Review.objects.filter(title=title_id).all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        current_title = get_object_or_404(Title, pk=title_id)
        current_user = self.request.user
        serializer.save(title=current_title, author=current_user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comment.objects.filter(review=review_id).all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        current_review = get_object_or_404(Review, pk=review_id)
        current_user = self.request.user
        serializer.save(review=current_review, author=current_user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,) # Изменил пермишн с IsAdminOrReadOnl.


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
            user = User.objects.get(username=registration_username)
            confirmation_code = default_token_generator.make_token(user)
            user.password = confirmation_code
            user.save()
            send_mail(
                subject='Код подтверждения регистрации.',
                message=f'Ваш код для регистрации: {confirmation_code}',
                from_email='test@mail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(
                {'email': registrstion_email, 'username': registration_username},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            password=request.data.get('confirmation_code')
        )
        if user.exists():
            try:
                token = RefreshToken.for_user(user[0])
                return Response(
                    {'access': str(token.access_token)},
                    status=status.HTTP_200_OK
                )
            except exceptions.ValidationError:
                return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_404_NOT_FOUND)


class UsersMeView(RetrievDeleteViewSet):
    serializer = serializers.UserSerializer

    def get_queryset(self):
        pass