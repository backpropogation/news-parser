from django.test import TransactionTestCase

from apps.parser.models import Site, News
from apps.parser.tasks import start_parsing

PASMI_NEWS_COUNT = 65


class ParsingTestCase(TransactionTestCase):
    def test_parsing_site(self):
        """
        Test parsing.
        """

        # bulk_create in order not calling .save() and triggering post_save signal.
        Site.objects.bulk_create(
            [
                Site(
                    url='https://pasmi.ru/',
                    news_css='div.post',
                    title_css='div.content h2 a',
                    sub_title_css='div.content p',
                    description_css='div.content p',
                    link_css='div.content h2 a',
                    time_css='div.content div.meta span.time',
                )
            ]
        )
        start_parsing.apply(args=(Site.objects.first().id,))
        self.assertAlmostEqual(News.objects.count(), PASMI_NEWS_COUNT, delta=5)
