from rest_framework import serializers

from apps.parser.models import Site


class SiteParsingSerializer(serializers.ModelSerializer):
    """
    Site serializer needed to serialize  objects.
    """
    news = serializers.CharField(source='news_css')
    title = serializers.CharField(source='title_css')
    sub_title = serializers.CharField(source='sub_title_css')
    description = serializers.CharField(source='description_css')
    time = serializers.CharField(source='time_css')
    link = serializers.CharField(source='link_css')

    class Meta:
        model = Site
        fields = (
            'news',
            'title',
            'sub_title',
            'description',
            'time',
            'link'
        )


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
