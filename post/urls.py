from django.urls import path
# from .views import PostListView, add_post, DeletePostView, PostDetailView, tags_list, tag_detail
from .views import index, add_post, post_detail, tags, like, update_post, delete_post

urlpatterns = [
    path('', index, name='post_list'),
    path('add/', add_post, name='add_post'),
    path('<uuid:post_id>/', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>', tags, name='tag'),
    path('<uuid:post_id>/like', like, name='post_like'),
    path('<uuid:post_id>/update', update_post, name='post_update'),
    path('delete/<uuid:post_id>/', delete_post, name='post_delete'),
    # path('user/', UserProfile, name='profile'),

]