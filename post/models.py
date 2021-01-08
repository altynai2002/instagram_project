from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', blank=True, null=True)
    caption = models.TextField()
    # likes = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    # slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})
# Если юзер удалит картинку, то в хранилище она тоже удалится
# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance):
#     instance.image.delete(False)
#
# def pre_save_blog_post_receiver(sender, instance):
#     if not instance.slug:
#         pass
