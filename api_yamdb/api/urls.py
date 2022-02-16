from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'titles', views.TitleViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
