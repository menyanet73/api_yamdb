from rest_framework import mixins, viewsets, permissions
from rest_framework.pagination import PageNumberPagination


class CreateDeleteListViewset(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    pass
