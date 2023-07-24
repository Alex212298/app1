from django.forms import ModelForm
from .models import Post

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['postAuthor', 'newsOrArt', 'postCategory', 'title', 'text']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get_or_create(name='common')[0]
        common_group.user_set.add(user)
        return user