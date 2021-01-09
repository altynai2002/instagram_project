from django.urls import path
# from .views import PostListView, add_post, DeletePostView, PostDetailView, UpdatePostView, tags_list, tag_detail
from .views import index, add_post, post_detail, tags, like

urlpatterns = [
    path('', index, name='post_list'),
    path('add/', add_post, name='add_post'),
    path('<uuid:post_id>/', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>', tags, name='tag'),
    path('<uuid:post_id>/like', like, name='post_like')
    # path('', PostListView.as_view(), name='post_list'),
    # # path('user/', UserProfile, name='profile'),


    # path('tag/<str:slug>/', tag_detail, name='tag_detail_url'),

    # path('update/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    # path('delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
]