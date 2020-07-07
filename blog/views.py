from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from product.models import Category


def index(request):
    return HttpResponse("Blog app")


def post_list(request):
    category = Category.objects.all()
    posts = Post.published.all()
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'blog.html', context)


def post_detail(request, year, month, day, post):
    category = Category.objects.all()
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    context = {
        'post': post,
        'category': category
    }
    return render(request, 'blog_detail.html', context)
