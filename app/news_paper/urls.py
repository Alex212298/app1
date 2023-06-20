from django.urls import path
from .views import *

urlpatterns = [
    path('news/', PostList.as_view()),
    path('news/<int:pk>/', PostOne.as_view()),
]