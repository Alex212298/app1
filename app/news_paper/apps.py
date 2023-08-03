from django.apps import AppConfig


class NewsPaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_paper'

    # def ready(self):
    #     import news_paper.signals
