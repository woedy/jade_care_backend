from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post, PostFile

User = get_user_model()

def articles_page_pat(request):
    context = {}

    articles = Post.objects.all().order_by('-created_at')

    context['all_articles'] = articles

    return render(request, 'posts/articles_pat.html', context)


def article_detail_page_pat(request, article_id):
    context = {}

    article = get_object_or_404(Post, id=article_id)

    context['article'] = article

    return render(request, 'posts/article_detail_pat.html', context)



def articles_page_doc(request):
    context = {}

    articles = Post.objects.all().order_by('-created_at')

    context['all_articles'] = articles

    return render(request, 'posts/articles_doc.html', context)


def articles_page_admin(request):
    context = {}

    articles = Post.objects.all().order_by('-created_at')

    context['all_articles'] = articles

    return render(request, 'posts/articles_admin.html', context)

def article_detail_page_doc(request, article_id):
    context = {}

    article = get_object_or_404(Post, id=article_id)

    context['article'] = article

    return render(request, 'posts/article_detail_doc.html', context)

def article_detail_page_admin(request, article_id):
    context = {}

    article = get_object_or_404(Post, id=article_id)

    context['article'] = article

    return render(request, 'posts/article_detail_admin.html', context)


def add_article_page_doc(request):
    context = {}

    articles = Post.objects.all().order_by('-created_at')
    context['all_articles'] = articles

    user = get_object_or_404(User, id=request.user.id)

    return render(request, 'posts/add_article_doc.html')

def add_article_post(request):
    context = {}

    user = get_object_or_404(User, id=request.user.id)

    if request.POST and request.FILES:
        name = request.POST.get('name')
        body = request.POST.get('body')
        files = request.FILES.getlist('files[]')


        print(name)
        print(body)
        print(files)


        new_article = Post.objects.create(
            name=name,
            body=body,
            author=user,
        )
        new_article.save()

        if files != None:
            for file in files:
                new_image = PostFile.objects.create(
                    post=new_article,
                    file=file
                )
                new_image.save()

    return redirect('posts:all_articles_doc')


def add_article_page_admin(request):
    context = {}

    articles = Post.objects.all().order_by('-created_at')
    context['all_articles'] = articles

    user = get_object_or_404(User, id=request.user.id)


    if request.method == "POST":
        print(request.POST)
        name = request.POST['name']
        body = request.POST['body']

        if name != None:
            new_article = Post.objects.create(
                name=name,
                body=body,
                author=user,
            )
            new_article.save()


        return render(request, 'posts/articles_admin.html', context)

    return render(request, 'posts/add_article_admin.html')