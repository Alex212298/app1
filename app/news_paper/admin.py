from django.contrib import admin
from django.contrib.sites.models import Site
from .models import *

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)


# Register your models here.
