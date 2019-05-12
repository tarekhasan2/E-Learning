

from django.contrib import admin
from django.urls import path

from . import views
app_name = "lessons"

urlpatterns = [
    
	path('<int:id>/lesson_details', views.lesson_details, name = 'details'),
	path('<int:id>/details/lesson_create', views.lesson_create, name = 'create'),
	path('<int:id>/lesson_update', views.lesson_update, name = 'update'),
	path('<int:id>/lesson_delete', views.lesson_delete, name = 'delete'),

]
