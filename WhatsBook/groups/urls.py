from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [

    path('list/', views.GroupListView.as_view(), name='group_list'),
    path('search_list/', views.SearchListView, name='search_list'),
    path('details/(?P<pk>[-\w]+)/', views.GroupDetailView.as_view(), name='group_details'),
    path('group/(?P<pk>\d+)/edit/', views.UpdateGroup.as_view(), name='group_update'),
    path('group/(?P<pk>\d+)/delete/', views.DeleteGroup.as_view(), name='group_delete'),
    path('create/', views.CreateGroup.as_view(), name='create_group'),
    path('add/', views.JoinGroup, name="add_member"),
    path('remove/', views.LeaveGroup, name="remove_member"),
    path("group_members/(?P<pk>\d+)", views.Groupmem.as_view(), name="group_members")

]