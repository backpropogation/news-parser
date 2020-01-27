import datetime
import hashlib

from django.core.cache import cache
from django.core.mail import send_mail

from parsing.celery import app
from django.template.loader import render_to_string


@app.task
def send_activation_url(username, email, webhook_url, resend=False):
    if resend:
        hash_string = cache.get(f'{username}_activation_link', None)
        cache.set(f'{username}_activation_link_resent', True, timeout=60 ** 3)
    else:
        hash_string = hashlib.md5(f"{email}{str(datetime.datetime.now())}".encode()).hexdigest()
        cache.set(hash_string, username, timeout=None)  # ДЛя вебхука
        cache.set(f'{username}_activation_link', hash_string,
                  timeout=60 ** 3 * 24 * 7)  # для нахождения ссылки привязанной к юзеру
    # Hard code url
    msg = render_to_string('email-confirm.html')
    activation_url = f"{webhook_url}?confirm={hash_string}"
    send_mail(
        'Resent' if resend else 'Your activation link',
        activation_url,
        'jack.moriarty@mail.ru',
        [email],
        fail_silently=False,
        html_message=msg
    )
