from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),

    # articles

    path('articles/', views.get_articles, name='articles'),
    path('articles/edit/<article_id>/', views.edit_articles, name='editArticles'),
    path('articles/create/', views.create_articles, name='createArticles'),
    path('articles/delete/<article_id>', views.delete_articles, name='deleteArticles'),
    path('article/view/<slug>', views.view_article, name='viewArticle'),

    #fim articles

    # categories

    path('categories/', views.get_categories, name='categories'),
    path('categories/edit/<category_id>/', views.edit_category, name='editCategory'),
    path('categories/create/', views.create_category, name='createCategory'),
    path('categories/delete/<category_id>', views.delete_category, name='deleteCategory'),

    #fim articles
]
