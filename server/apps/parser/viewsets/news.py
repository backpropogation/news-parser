from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.parser.filters import NewsFilter
from django_filters import rest_framework as filters
from apps.parser.models import News
from apps.parser.serializers import NewsReadSerializer


class NewsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class NewsViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Endpoint for dealing with site objects.
    """
    pagination_class = NewsSetPagination
    serializer_class = NewsReadSerializer
    queryset = News.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
