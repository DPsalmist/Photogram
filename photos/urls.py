from django.urls import path
from . import views 
from .feeds import LatestPhotoFeed
from .views import (
 #PhotoListView, 
 PhotoDetailView,
 PhotoCreateView,
 PhotoUpdateView,
 PhotoDeleteView,
 UserPhotoListView,
 SearchResultsView
 )

urlpatterns = [
	path('', views.gallery, name='gallery'),
	path('about/', views.aboutPage, name='about'),
	path('photo/<str:pk>/', views.viewPhoto, name='photo_detail'),
	#path('user/<str:username>/', views.userPhotoList, name='user_photos'),
	#path('add/', views.addPhoto, name='add'),
	path('search/', SearchResultsView.as_view(), name='search_results'),
	path('feed/', LatestPhotoFeed(), name='photo_feed'),


	#path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPhotoListView.as_view(), name='user_pics'),
    #path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/update', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete', PhotoDeleteView.as_view(), name='photo_delete'),
    path('add/new/', PhotoCreateView.as_view(), name='add'),
]