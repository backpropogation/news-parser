from django.db import models


class Site(models.Model):
    """
    This entity represents site to be parsed.
    """

    url = models.URLField(
        verbose_name='Site\'s url'
    )
    news_css = models.CharField(
        max_length=255,
        verbose_name='CSS path to piece of news tag'
    )
    title_css = models.CharField(
        max_length=255,
        verbose_name='CSS path (inside news tag) to title'
    )
    sub_title_css = models.CharField(
        max_length=255,
        verbose_name='CSS path (inside news tag) to subtitle'
    )
    description_css = models.CharField(
        max_length=255,
        verbose_name='CSS path (inside news tag) to description'
    )
    link_css = models.CharField(
        max_length=255,
        verbose_name='CSS path (inside news tag) to link'
    )
    time_css = models.CharField(
        max_length=255,
        verbose_name='CSS path (inside news tag) to publication date'
    )

    def __str__(self):
        return self.url
