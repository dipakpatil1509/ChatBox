from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [

    path('', views.UserListView, name='user_list'),
    path('search/', views.SearchListPost, name='search_list'),
]

