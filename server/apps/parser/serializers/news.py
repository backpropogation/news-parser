from rest_framework import serializers
from apps.parser.models import News


class NewsReadSerializer(serializers.ModelSerializer):
    """
    Site serializer needed to serialize news objects.
    """

    site = serializers.SerializerMethodField()
    parsed_at = serializers.DateTimeField(format='%D %H:%M:%S')

    class Meta:
        model = News
        exclude = ('id',)

    def get_site(self, obj):
        return obj.site.url
