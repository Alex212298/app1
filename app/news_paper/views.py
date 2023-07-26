from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .filters import PostFilter
from .forms import PostForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.models import Group
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives

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

    def form_valid(self, form):
        self.object = form.save()

        self.postCategory_list = self.object.postCategory.all()

        for category in self.postCategory_list:

            for sub in category.subscribes.all():
                html_content = render_to_string('post_created.html',
                                                {
                                                    'user': sub,
                                                    'post': self.object,
                                                })

                msg = EmailMultiAlternatives(
                    subject=f'{self.object.title}',
                    body=self.object.text,
                    from_email='rassylkovna@yandex.ru',
                    to=[f'{sub.email}']

                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('news')


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


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'cat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['subscribers'] = category.subscribes.all()
        return context


def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribes.add(request.user.id)
    return HttpResponseRedirect(reverse('cat', args=[pk]))


def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribes.remove(request.user.id)
    return HttpResponseRedirect(reverse('cat', args=[pk]))
