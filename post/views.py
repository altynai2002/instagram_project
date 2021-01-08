from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from .forms import PostForm, AddPostForm, UpdatePostForm
from .models import Post, Tag

class PostListView(ListView):

    template_name = 'post/post_list.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

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
        form = PostForm()
    return render(request, 'post/post_create.html', {'form': form})

class ViewsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

class UpdatePostView(ViewsMixin, UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    form_class = UpdatePostForm

class DeletePostView(DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post_list')

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'post/tag.html',)


