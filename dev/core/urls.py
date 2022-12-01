from django.urls import path
from . import views

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('signup', views.user_signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('projs', views.ProjectListView.as_view(), name='projs'),
    path('acts', views.ActionListView.as_view(), name='acts'),
    path('proj/new/', views.ProjectCreateView.as_view(), name='proj-new'),
    path('proj/<int:pk>/', views.ProjectUpdateView.as_view(), name='proj-detail'),
    path('proj/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='proj-update'),
    path('proj/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='proj-delete'),
    path('act/new/', views.ActionCreateView.as_view(), name='act-new'),
    path('act/<int:pk>/', views.ActionUpdateView.as_view(), name='act-detail'),
    path('act/<int:pk>/update/', views.ActionUpdateView.as_view(), name='act-update'),
    path('act/<int:pk>/delete/', views.ActionDeleteView.as_view(), name='act-delete'),
    path('files', views.FileListView.as_view(), name = 'files'),
    path('tags', views.TagListView.as_view(), name='tags'),
    path('tag/new/', views.TagCreateView.as_view(), name='tag-new'),
    path('tag/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag-delete'),
]

