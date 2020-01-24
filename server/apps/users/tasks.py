import datetime
import hashlib

from django.core.cache import cache
from django.core.mail import send_mail

from parsing.celery import app


@app.task
def send_activation_url(username, email, webhook_url):
    hash_string = hashlib.md5(f"{email}{str(datetime.datetime.now())}".encode()).hexdigest()
    # Hard code url
    activation_url = f"{webhook_url}?confirm={hash_string}"
    cache.set(hash_string, username, timeout=None)
    send_mail(
        'Your activation link',
        activation_url,
        'jack.moriarty@mail.ru',
        [email],
        fail_silently=False,
    )
