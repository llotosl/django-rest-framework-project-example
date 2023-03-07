from django.db import models


class News(models.Model):
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(max_length=2000)

    likes = models.ManyToManyField('users.CustomUser', through='news.NewsLike')
    comments = models.ManyToManyField(
        'news.Comment', through='news.NewsComment')


class NewsLike(models.Model):
    news = models.ForeignKey('news.News', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    parent_comment = models.ForeignKey(
        'news.Comment', on_delete=models.SET_NULL, null=True)


class NewsComment(models.Model):
    news = models.ForeignKey('news.News', on_delete=models.CASCADE)
    comment = models.ForeignKey('news.Comment', on_delete=models.CASCADE)
