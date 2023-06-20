from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная страница'}
    queryset = Post.objects.order_by('-dateCreate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostOne(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'one_news'
    extra_context = {'title': 'Новость'}
