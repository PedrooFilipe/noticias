from django.contrib import admin

# Register your models here.
from news.models import Article
from news.models import Comment


# class ArticleAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Article)