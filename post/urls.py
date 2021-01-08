from django.urls import path
from .views import PostListView, add_post, DeletePostView, PostDetailView, UpdatePostView, tags_list

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    # path('user/', UserProfile, name='profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('tags/', tags_list, name='tags_list_url'),
    path('add/', add_post, name='add_post'),
    path('update/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
]