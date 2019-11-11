from django.contrib import admin
from apps.parser.models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass
