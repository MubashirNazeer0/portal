from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchUserView,
    welcome,
    manage_pending_profiles,posters_list,add_posters
    
)
from . import views

urlpatterns = [
    
    path('', views.welcome, name='welcome'),

    path('manage_pending_profiles/', views.manage_pending_profiles, name='manage_pending_profiles'),
    path('home/', PostListView.as_view(), name='dash-home'),
    path('welcome/', views.welcome, name='welcome'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='dash-about'),
    path('search/', SearchUserView.as_view(), name='search-users'),
    path('add_advertisement/', views.add_advertisement, name='add_advertisement'),
    path('advertisements/', views.advertisement_list, name='advertisement_list'), 
    path('advertisements/<int:pk>/delete/', views.delete_advertisement, name='delete_advertisement'),
    path('add_posters/', views.add_posters, name='add_posters'),
    path('posters/', views.posters_list, name='posters_list'),  
    
    
    
]