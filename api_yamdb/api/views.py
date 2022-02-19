from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination

from api import serializers
from api.permissions import IsUserOrAdmin
from .viewsets import CreateDeleteListViewset
from reviews.models import Title, Genre, Category, Review, Comment, User


class GenreViewSet(CreateDeleteListViewset):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'


class CategoryViewSet(CreateDeleteListViewset):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'


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
