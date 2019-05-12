
from django.contrib import admin
from django.urls import path
from . import views
app_name = "blogs"

urlpatterns = [
    
	path('posts/', views.postHome, name = 'list'),
	path('posts/<int:id>/details', views.postDetails, name = 'details'),
	path('posts/create', views.postCreate, name = 'create'),
	path('posts/<int:id>/update', views.postUpdate, name = 'update'),
	path('posts/<int:id>/delete', views.postDelete, name = 'delete'),

]
