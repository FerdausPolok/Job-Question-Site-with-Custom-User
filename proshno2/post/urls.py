from django.contrib import admin

from django.urls import path, include
from post import urls as post_urls
from post.views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, post_details

app_name= 'post'


urlpatterns = [
    #path('', post_list, name='post_list'),
    path('',PostListView.as_view(), name='post_list'),
    path('<int:post_id>/', post_details, name='post_details'),
    #path('<int:pk>/', PostDetailView.as_view(), name='post_details'),
    #path('post-create/', post_create, name='post_create'),
    path('post-create/', PostCreateView.as_view(), name='post_create'),

    #path('post-update/<int:post_id>/', post_update, name='post_update'),
    path('post-update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    #path('post-delete/<int:post_id>/', post_delete, name='post_delete'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

]
