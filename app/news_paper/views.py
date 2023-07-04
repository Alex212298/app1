from datetime import datetime

from .filters import PostFilter
from .forms import PostForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from .models import *


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная страница'}
    queryset = Post.objects.order_by('-dateCreate')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Post.objects.all().count()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)



class PostSearch(PostList):
    template_name = 'news_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostOne(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'one_news'
    extra_context = {'title': 'Новость'}

class PostCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'