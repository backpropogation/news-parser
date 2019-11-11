from rest_framework.routers import DefaultRouter

from apps.parser.viewsets import NewsViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, base_name='news')
