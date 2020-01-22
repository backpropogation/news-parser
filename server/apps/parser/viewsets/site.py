from rest_framework import viewsets
from rest_framework import mixins
from apps.parser.models import Site
from apps.parser.serializers import SiteSerializer


class SiteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()


