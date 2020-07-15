from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Post, Author, Blog_Category
from product.models import Category


def index(request, category_slug=None):
    blog = "blog"
    category = None
    categories = Blog_Category.objects.all()
    post_list = Post.published.all()
    if category_slug:
        category = get_object_or_404(Blog_Category, slug=category_slug)
        post_list = post_list.filter(category=category)
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'category': category,
        'categories': categories,
        'page_request_var': page_request_var,
        'blog': blog,
    }
    return render(request, 'blog.html', context)


def post_detail(request, year, month, day, post):
    author = Author.objects.get(pk=1)
    category = Category.objects.all()
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            messages.success(request, "Your Comment has been sent. Thanks for your Comment")
            return HttpResponseRedirect(url)
    else:
        comment_form = CommentForm()
    context = {
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments': comments,
        'author': author,
        'post': post,
        'category': category
    }
    return render(request, 'blog_detail.html', context)


def searches(request):
    category = Category.objects.all()
    if request.method=='POST':
        srch = request.POST['srh']

        if srch:
            match = Post.objects.filter(Q(title__icontains=srch) |
                                        Q(overview__icontains=srch)
                                        )
            if match:
                return render(request, 'blogsearch.html', {'sr': match, 'category': category})
            else:
                messages.error(request, 'No result Found')
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'blogsearch.html', {'sr': match, 'category': category})


