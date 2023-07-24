from django.urls import path
from .views import *

urlpatterns = [
    path('news/', PostList.as_view()),
    path('news/<int:pk>/', PostOne.as_view()),
    path('news/search/', PostSearch.as_view()),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('add_to_group/', add_to_group, name='add_to_group'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='cat'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe, name='unsubscribe'),
]