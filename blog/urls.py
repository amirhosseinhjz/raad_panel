from django.urls import path
from blog.views import BlogPostListView

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='home'),
]
