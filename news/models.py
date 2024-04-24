from django.db import models


# Create your models here.

class Category(models.Model):
    description = models.CharField(max_length=100)
    shouldBeDisplayed = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)


class Article(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True)
    text = models.TextField()
    slug = models.TextField(50)
    posted = models.DateTimeField(null=True)
    thumb = models.ImageField(upload_to='img', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    highlight = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=70)
    text = models.TextField()
