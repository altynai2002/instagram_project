from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from comment.forms import CommentForm
from comment.models import Comment
from .forms import AddPostForm, UpdatePostForm
from .models import Post, Tag, Stream, Likes


@login_required
def index(request):
    author = request.user
    posts = Stream.objects.filter(user=author)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-created_date')
    return render(request, template_name='post/post_list.html', context={'post_items': post_items})

@login_required(login_url='login')
def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = AddPostForm
    return render(request, 'post/post_create.html', context={'form': form})

@login_required(login_url='login')
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = UpdatePostForm(instance=post)

    if request.method == "POST":
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_list")

    return render(request, "post/post_update.html", {'form': form})

@login_required(login_url='login')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("post_list")

@login_required(login_url='login')
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    comments = Comment.objects.filter(post=post).order_by('date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
    else:
        form = CommentForm()

    return render(request, 'post/post_detail.html', context={'post': post, 'form': form, 'comments':comments})

@login_required(login_url='login')
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_date')

    return render(request, 'post/tag.html', context={'posts': posts, 'tag': tag})

@login_required(login_url='login')
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post_list'))

# def searcher(request):
#     if request.method == 'GET':
#         search = request.GET.get('search')
#         user = User.objects.all().filter(username=search)
#         return render(request, 'post/searchbar.html', {'user': user})
#
