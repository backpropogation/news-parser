from rest_framework.routers import DefaultRouter

from apps.parser.viewsets import NewsViewSet, SiteViewSet
from apps.users.viewsets import RegisterViewSet, LoginViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('sites', SiteViewSet, basename='sites')
router.register('register', RegisterViewSet, basename='register')
router.register('login', LoginViewSet, basename='login')
