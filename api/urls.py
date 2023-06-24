from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('all-posts/', views.GetAllPosts.as_view(), name='all_posts'), # Endpoint to retrieve all posts
    path('post/<post_id>/', views.OnePost.as_view(), name='one_post'), # Endpoint to retrieve a specific post by post_id
    path('manage-post/<post_id>/', views.MangePost.as_view(), name='manage_post'), # Endpoint to manage (update/delete) a specific post by post_id
    path('add-post/', views.AddPost.as_view(), name='add_post'), # Endpoint to add a new post
]