
from django.contrib import admin
from django.urls import path
from . import views
app_name = "comments"

urlpatterns = [
	path('posts/<int:id>/', views.reply, name = 'comments'),
	path('posts/<int:id>/delete', views.delete_comment, name = 'delete_comment'),

]
