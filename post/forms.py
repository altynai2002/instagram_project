from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'caption')

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'caption', 'tags')

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'caption', 'tags')

    def save(self, commit=True):
        post = self.instance
        post.caption = self.cleaned_data['caption']

        if self.cleaned_data['image']:
            post.image = self.cleaned_data['image']

        if commit:
            post.save()
        return post

