from django.db import models


class News(models.Model):
    """
    This entity represents piece of news with all general parts.
    """

    title = models.CharField(
        max_length=255,
        null=True,
        unique=True,
        verbose_name='Title'
    )
    sub_title = models.CharField(
        max_length=1255,
        null=True,
        verbose_name='Subtitle'
    )
    description = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Description'
    )
    time = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Publication date'
    )
    link = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Link'
    )
    site = models.ForeignKey(
        'parser.Site',
        on_delete=models.CASCADE,
        verbose_name='Site'
    )

    parsed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Parsed at'
    )

    def __str__(self):
        return self.title
