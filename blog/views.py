from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import BlogPost, Blogger
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm

def index(request):
    # simple index describing the site and links
    return render(request, 'blog/index.html')

def blog_list(request):
    posts = BlogPost.objects.select_related('author').all()
    paginator = Paginator(posts, 5)  # paginated in groups of 5
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost.objects.select_related('author'), pk=pk)
    comments = post.comments.select_related('author').all()  # oldest -> newest per Meta
    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments})

def blogger_list(request):
    bloggers = Blogger.objects.all()
    return render(request, 'blog/blogger_list.html', {'bloggers': bloggers})

def blogger_detail(request, pk):
    blogger = get_object_or_404(Blogger, pk=pk)
    posts = blogger.posts.all()  # ordering set on BlogPost Meta -> newest first


    return render(request, 'blog/blogger_detail.html', {'blogger': blogger, 'posts': posts})
    

    

@login_required
def create_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            c.save()
            return redirect('blog:blog_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/create_comment.html', {'form': form, 'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: create blogger profile automatically
            Blogger.objects.create(user=user, name=user.username)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib import messages
from .forms import BlogPostForm

@login_required
# def create_post(request):
#     # Ensure the user has a Blogger profile
#     blogger = getattr(request.user, 'blogger', None)
#     if not blogger:
#         messages.error(request, "You must be a registered blogger to create posts.")
#         return redirect('blog:index')

#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = blogger
#             post.save()
#             messages.success(request, "Your post was created successfully!")
#             return redirect('blog:blog_detail', pk=post.pk)
#     else:
#         form = BlogPostForm()

#     return render(request, 'blog/create_post.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            blogger, created = Blogger.objects.get_or_create(user=request.user)
            post.author = blogger
            post.save()
            return redirect('blog:blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # or any other page

