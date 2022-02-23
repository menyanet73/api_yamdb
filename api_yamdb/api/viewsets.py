from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly


class CreateDeleteListViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)



class RetrieveUpdateViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
