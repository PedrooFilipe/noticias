from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Category


def index(request):
    categories = Category.objects.filter(shouldBeDisplayed=True)
    articles = Article.objects.all()
    highlight = Article.objects.filter(highlight=True).order_by('timestamp').first()
    return render(request, 'news/Portal/Index.html', context={
                                                        'categories': categories,
                                                        'articles': articles,
                                                        'highlight': highlight
                                                    })


def login(request):
    return render(request, 'news/login.html')


# articles
def get_articles(request):
    return render(request, 'news/Articles/Index.html',
                  context={'articles': Article.objects.all()})


def search_articles(request, search):
    articles = Article.objects.filter()
    return render(request, 'news/Articles/Index.html',
                  context={'articles': Article.objects.all()})


def view_article(request, slug):
    categories = Category.objects.filter(shouldBeDisplayed=True)
    article = Article.objects.get(slug=slug)
    articles = Article.objects.filter(
        (Q(category__description=article.category.description) & ~Q(id=article.id)))
    return render(request, 'news/Portal/ViewArticle.html', context={'article': article,
                                                                    'articles': articles,
                                                                    'categories': categories})


def edit_articles(request, article_id=None):
    article = get_object_or_404(Article, id=article_id)

    if 'save_article' in request.POST:
        article.title = request.POST.get('title', '')
        article.slug = request.POST.get('slug', '')
        article.text = request.POST.get('text', '')
        article.thumb = request.FILES.get('image', '')

        if (request.POST.get('category', '')):
            article.category = Category.objects.get(id=request.POST.get('category'))

        article.save()

        return redirect('articles')

    else:
        if article.category:
            categories = Category.objects.filter(~Q(id=article.category.id)).values()
        else:
            categories = Category.objects.all()
        return render(request, 'news/Articles/Form.html',
                      context={'article': article,
                               'categories': categories})


def create_articles(request):
    global category
    print(request.POST)
    if 'save_article' in request.POST:

        if (request.POST.get('category', '')):
            category = Category.objects.get(id=request.POST.get('category'))

        # print(request.POST.get('highlight', ''))
        article = Article(title=request.POST.get('title', ''), slug=request.POST.get('slug', ''),
                          text=request.POST.get('text', ''), category=category,  highlight=request.POST.get('highlight', ''),
                          thumb=request.FILES.get('image', ''))

        article.save()

        return redirect('articles')
    else:
        return render(request, 'news/Articles/Form.html', context={'categories': Category.objects.all()})


def delete_articles(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    article.delete()

    return redirect('articles')


# end articles

# articles
def get_categories(request):
    return render(request, 'news/Categories/Index.html',
                  context={'categories': Category.objects.all()})


def edit_category(request, category_id=None):
    category = get_object_or_404(Category, id=category_id)

    if 'save_category' in request.POST:
        category.description = request.POST.get('description', '')

        category.save()

        return redirect('categories')

    else:
        return render(request, 'news/Categories/Form.html',
                      context={'category': category})


def create_category(request):
    if 'save_category' in request.POST:
        category = Category(description=request.POST.get('description', ''))
        category.save()

        return redirect('categories')
    else:

        return render(request, 'news/Categories/Form.html')


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    category.delete()

    return redirect('categories')

# end articles
