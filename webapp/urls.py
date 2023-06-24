from django.urls import path

from webapp import views

app_name = 'webapp'
urlpatterns = [
    path('', views.PostListView.as_view(), name='home'), # the home page endpoint
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail' ), # a single post endpoint
]
