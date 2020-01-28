from django_filters import rest_framework as filters

from apps.parser.models import News, Site


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    description = filters.CharFilter(field_name="description", lookup_expr='icontains')
    sub_title = filters.CharFilter(field_name="sub_title", lookup_expr='icontains')
    site = filters.ModelChoiceFilter(field_name="site", to_field_name='url', queryset=Site.objects.all())

    class Meta:
        model = News
        fields = ('title', 'description', 'sub_title', 'site', 'parsed_at')
