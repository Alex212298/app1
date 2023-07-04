from django.urls import path
from .views import *

urlpatterns = [
    path('news/', PostList.as_view()),
    path('news/<int:pk>/', PostOne.as_view()),
    path('news/search/', PostSearch.as_view()),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
]