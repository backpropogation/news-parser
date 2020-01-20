from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
