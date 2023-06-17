from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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


class Category (models.Model):
    categoryName = models.CharField(max_length=65, unique=True)


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
