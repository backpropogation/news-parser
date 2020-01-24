from django.contrib import admin
from django.urls import include, path

from apps.parser.router import router
from des import urls as des_urls
from apps.users.viewsets import mail_confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('django-des/', include(des_urls)),
    path('confirm/', mail_confirm, name='email-confirm')
]
