from django.contrib import admin
from apps.parser.models import Site, News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass
