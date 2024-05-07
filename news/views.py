from django.contrib.auth import authenticate
from django.contrib.auth import login as djangoLogin
from django.contrib.auth import logout as djangoLogout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Category


def index(request):
    categories = Category.objects.filter(shouldBeDisplayed=True)
    articles = Article.objects.filter(highlight=False)[:3]
    highlight = Article.objects.filter(highlight=True).order_by('timestamp').first()
    more_reads = Article.objects.filter(viewCount__gt=0).order_by('viewCount')[:5]

    return render(request, 'news/Portal/Index.html', context={
        'categories': categories,
        'articles': articles,
        'highlight': highlight,
        'more_reads': more_reads
    })


def search_articles(request):
    search = print(request.GET.get('search', ''))
    if (search):
        articles = Article.objects.filter(title__contains=search)
    else:
        articles = Article.objects.all()

    return render(request, 'news/Portal/SearchArticles.html',
                  context={'articles': articles})


def view_article(request, slug):
    # categories = Category.objects.filter(shouldBeDisplayed=True)
    article = Article.objects.get(slug=slug)
    articles = Article.objects.filter(
        (Q(category__description=article.category.description) & ~Q(id=article.id)))

    article.viewCount += 1
    article.save()

    return render(request, 'news/Portal/ViewArticle.html', context={'article': article,
                                                                    'articles': articles})


def login(request):
    if (request.method == 'GET'):
        return render(request, 'news/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if (user):
        djangoLogin(request, user)
        return redirect('articles')
    else:
        return render(request, 'news/login.html', context={'message': 'Email ou senha incorreto'})


def logout(request):
    djangoLogout(request)
    return redirect('login')


# articles
@login_required(login_url='login')
def get_articles(request):
    articles = Article.objects.all()

    current_page = request.GET.get('page')

    paginator = Paginator(articles, 10)

    page = paginator.get_page(current_page)

    return render(request, 'news/Articles/Index.html',
                  context={'page': page})


@login_required(login_url='login')
def edit_articles(request, article_id=None):
    article = get_object_or_404(Article, id=article_id)

    if 'save_article' in request.POST:
        article.title = request.POST.get('title', '')
        article.slug = request.POST.get('slug', '')
        article.text = request.POST.get('text', '')
        if request.FILES.get('image', ''):
            article.thumb = request.FILES.get('image', '')

        if request.POST.get('category', ''):
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


@login_required(login_url='login')
def create_articles(request):
    global category
    if 'save_article' in request.POST:

        if (request.POST.get('category', '')):
            category = Category.objects.get(id=request.POST.get('category'))

        # print(request.POST.get('highlight', ''))
        article = Article(title=request.POST.get('title', ''), slug=request.POST.get('slug', ''),
                          text=request.POST.get('text', ''), category=category,
                          thumb=request.FILES.get('image', ''))

        article.save()

        return redirect('articles')
    else:
        return render(request, 'news/Articles/Form.html', context={'categories': Category.objects.all()})


@login_required(login_url='login')
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
