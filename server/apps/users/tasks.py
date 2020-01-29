import datetime
import hashlib

from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string

from parsing.celery import app


@app.task
def send_activation_url(username, email, webhook_url):
    hash_string = hashlib.md5(f"{email}{str(datetime.datetime.now())}".encode()).hexdigest()
    cache.set(hash_string, username, timeout=None)
    cache.set(f'{username}_activation_link', hash_string, timeout=60 ** 3 * 24 * 7)
    _send_mail_with_activation_link('email-confirm.html', email, hash_string, webhook_url, 'Activaion_link')


@app.task
def resend_activation_url(username, email, webhook_url):
    hash_string = cache.get(f'{username}_activation_link', None)
    cache.set(f'{username}_activation_link_was_resent', True, timeout=60 ** 3)
    _send_mail_with_activation_link('email-confirm.html', email, hash_string, webhook_url, 'Resend')


def _send_mail_with_activation_link(template_name, email, hash_string, webhook_url, title):
    msg = render_to_string(template_name=template_name)
    activation_url = f"{webhook_url}?confirm={hash_string}"
    send_mail(
        title,
        activation_url,
        'jack.moriarty@mail.ru',
        [email],
        fail_silently=False,
        html_message=msg
    )
