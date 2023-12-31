from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.cache import cache


class Author (models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)


    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        if postRat.get('postRating') == None:
            prat = 0
        else:
            pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        if commentRat.get('commentRating') == None:
            cRat = 0
        else:
            cRat += commentRat.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return self.authorUser.username


class Category (models.Model):
    categoryName = models.CharField(max_length=65, unique=True)
    subscribes = models.ManyToManyField(User, through='CategorySub')
    def __str__(self):
        return self.categoryName

class CategorySub(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}"
class Post (models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AC'
    NEWS_OR_ARTICLE_CHOICE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    newsOrArt = models.CharField(
        max_length=2,
        choices=NEWS_OR_ARTICLE_CHOICE,
        default=NEWS
    )

    dateCreate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:125]}..."

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class PostCategory (models.Model):
    postTR = models.ForeignKey(Post, on_delete=models.CASCADE)
    catTR = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    dateCreate = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
