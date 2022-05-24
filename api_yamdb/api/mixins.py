from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CustomMixinSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'
