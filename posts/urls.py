from django.urls import path


from .views import *

app_name = 'posts'

urlpatterns = [
    path('', postCommentAndListView, name='index'),
    path('like_unlike/', likeUnlikePostView, name='like-unlike'),
    path('delete/<pk>/', DeletePostView.as_view(), name='delete-post'),
    path('update/<pk>/', UpdatePostView.as_view(), name='update-post'),
]
