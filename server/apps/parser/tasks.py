import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.forms.models import model_to_dict
from selenium.webdriver.chrome.options import Options

from apps.parser.models import Site, SITE_FIELDS, News
from apps.parser.utils import text_or_none
from parsing.celery import app
from selenium import webdriver

@app.task
def start_parsing(site_id):
    """
    Task for parsing and creating news instances.
    """

    site = Site.objects.get(id=site_id)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(site.url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    selectors = {field.replace('_css', ''): css_path for field, css_path in model_to_dict(site, fields=SITE_FIELDS).items()}
    news_list = soup.select(selectors['news'])
    selectors.pop('news')
    for news in news_list:
        news_serialized = {
            field: text_or_none(news, field, css)
            for field, css in selectors.items()
        }
        try:
            News.objects.create(
                site=site, **news_serialized
            )
        except IntegrityError:
            pass



