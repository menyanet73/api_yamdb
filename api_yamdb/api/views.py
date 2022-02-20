from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator

from api import serializers
from api.permissions import IsUserOrAdmin
from .viewsets import CreateDeleteListViewset
from reviews.models import Title, Genre, Category, Review, Comment, User
from api_yamdb.settings import SIMPLE_JWT


class GenreViewSet(CreateDeleteListViewset):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'
    search_fields = ['name',]


class CategoryViewSet(CreateDeleteListViewset):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    search_fields = ['name',]
    

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Review.objects.filter(title=title_id).all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        current_title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=current_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comment.objects.filter(review=review_id).all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        current_review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=current_review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination
    permission_classes = (IsUserOrAdmin,)


class AuthUserView(APIView):
    def post(self, request):
        serializer = serializers.AuthUserSerializer(data=request.data)
        registration_username = request.data['username']
        registrstion_email = request.data['email']
        if registration_username == 'me':
            raise ValueError('Нельзя использовать это имя.')
        list_emails = User.objects.values_list('email', flat=True)
        if registrstion_email in list_emails:
            raise ValueError(
                f'''e-mail: {registrstion_email} уже зарегистрирован.
                Используйте другой email''')
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
                f'Код подтверждения отправлен на почту {email}',
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateToken(APIView):
    def post(self, request):
        pass
