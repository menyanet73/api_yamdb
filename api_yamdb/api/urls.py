from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'titles', views.TitleViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'users', views.UserViewSet, basename='users')

router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/auth/signup/', views.SignUpUserView.as_view(), name='signup'),
    path('v1/auth/token/', views.CreateUserToken.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
