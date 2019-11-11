from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from apps.parser.models import News
from apps.parser.serializers import NewsReadSerializer


class NewsViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    """
    Endpoint for dealing with site objects.
    """

    serializer_class = NewsReadSerializer
    queryset = News.objects.all()





