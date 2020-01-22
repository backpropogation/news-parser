from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.parser.models import Site
from apps.parser.tasks import start_parsing


@receiver(post_save, sender=Site)
def init_parsing(instance, **kwargs):
    """
    Post save signal needed to start task in the background after creating site object.
    """
    if instance.pk is not None:
        start_parsing.delay(instance.id)
