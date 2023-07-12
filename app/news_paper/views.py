from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect

from .filters import PostFilter
from .forms import PostForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.models import Group

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



class PostSearch(LoginRequiredMixin, PostList):
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

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    permission_required = ('news_paper.add_post')
    form_class = PostForm

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    permission_required = ('news_paper.update_post')
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_paper.delete_Post')
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'




def add_to_group(request):
    user = request.user
    group = Group.objects.get(name='authors')
    Author.objects.create(authorUser=User.objects.get(username=user.username))
    user.groups.add(group)
    return redirect('/news/')
