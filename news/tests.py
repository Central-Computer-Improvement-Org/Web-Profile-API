from django.test import TestCase

from news.news_models import News
from news.detail_news_media_models import DetailNewsMedia


def _create_news(id, title, description, media_uri):
    News.objects.create(id=id, title=title, description=description, media_uri=media_uri)


def _create_detail_news_media(id, title, news_id, description, media_uri):
    DetailNewsMedia.objects.create(id=id, title=title, news_id=news_id, description=description, media_uri=media_uri)


class NewsTestCase(TestCase):

    def setUp(self):
        _create_news('1', 'title1', 'description1', 'media_uri1')
        _create_news('2', 'title2', 'description2', 'media_uri2')
        _create_news('3', 'title3', 'description3', 'media_uri3')

        news1 = News.objects.get(id='1')
        news2 = News.objects.get(id='2')
        news3 = News.objects.get(id='3')

        _create_detail_news_media('1', 'title1', news1, 'description1', 'media_uri1')
        _create_detail_news_media('2', 'title2', news2, 'description2', 'media_uri2')
        _create_detail_news_media('3', 'title3', news3, 'description3', 'media_uri3')

    def test_news(self):
        news = News.objects.get(id='1')
        self.assertEqual(news.title, 'title1')
        self.assertEqual(news.description, 'description1')
        self.assertEqual(news.media_uri, 'media_uri1')

        news = News.objects.get(id='2')
        self.assertEqual(news.title, 'title2')

        news = News.objects.get(id='3')
        self.assertEqual(news.title, 'title3')

    def test_detail_news_media(self):
        detail_news_media = DetailNewsMedia.objects.get(id='1')
        self.assertEqual(detail_news_media.news_id.id, '1')
        self.assertEqual(detail_news_media.media_uri, 'media_uri1')

        detail_news_media = DetailNewsMedia.objects.get(id='2')
        self.assertEqual(detail_news_media.news_id.id, '2')
        self.assertEqual(detail_news_media.media_uri, 'media_uri2')

        detail_news_media = DetailNewsMedia.objects.get(id='3')
        self.assertEqual(detail_news_media.news_id.id, '3')
        self.assertEqual(detail_news_media.media_uri, 'media_uri3')