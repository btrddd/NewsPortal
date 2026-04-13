from django.apps import AppConfig


class NewsFeedConfig(AppConfig):
    name = 'news_feed'


    def ready(self):
        import news_feed.signals