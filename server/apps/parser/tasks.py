import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.forms.models import model_to_dict

from apps.parser.models import Site, NEWS_FIELDS, News
from apps.parser.utils import text_or_none
from parsing.celery import app


@app.task
def start_parsing(site_id):
    """
    Task for parsing and creating news instances.
    """

    site = Site.objects.get(pk=site_id)
    page = requests.get(site.url)
    soup = BeautifulSoup(page.text, 'html.parser')
    selectors = model_to_dict(site, fields=NEWS_FIELDS)
    news_list = soup.select(selectors['news_css'])
    selectors.pop('news_css')
    for news in news_list:
        news_serialized = {
            field.replace('_css', ''): text_or_none(news, field, css)
            for field, css in selectors.items()
        }
        try:
            News.objects.create(
                site=site, **news_serialized
            )
        except IntegrityError:
            pass



