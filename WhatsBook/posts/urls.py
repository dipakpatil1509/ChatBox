from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [

    path("create/", views.CreatePost, name="post_create"),
    path("deletepost/(?P<id>\d+)/", views.DeletePost, name="post_delete"),

]