from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import PostForm, AddPostForm, UpdatePostForm
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
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'post/post_detail.html', context={'post': post})

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

    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))



#
# class ViewsMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post_form'] = self.get_form(self.get_form_class())
#         return context
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
# class UpdatePostView(ViewsMixin, UpdateView):
#     model = Post
#     template_name = 'post/post_update.html'
#     form_class = UpdatePostForm
#
# class DeletePostView(DeleteView):
#     model = Post
#     template_name = 'post/post_delete.html'
#     success_url = reverse_lazy('post_list')
#
# def tags_list(request):
#     tags = Tag.objects.all()
#     return render(request, 'post/tag.html', context={'tags': tags})
#
# def tag_detail(request, slug):
#     tag = Tag.objects.get(slug__iexact=slug)
#     return render(request, 'post/tag_detail.html', context={'tag': tag})
#
#
