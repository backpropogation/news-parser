from django_filters import rest_framework as filters

from apps.parser.models import News


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    description = filters.CharFilter(field_name="description", lookup_expr='icontains')
    sub_title = filters.CharFilter(field_name="sub_title", lookup_expr='icontains')
    site = filters.CharFilter(field_name="site__url", lookup_expr='icontains')

    class Meta:
        model = News
        fields = ('title', 'description', 'sub_title', 'site', 'parsed_at')
