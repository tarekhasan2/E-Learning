

from django.contrib import admin
from django.urls import path

from . import views
app_name = "courses"

urlpatterns = [
    
	path('', views.courses, name = 'list'),
	path('<int:id>/details', views.course_details, name = 'details'),
	path('create', views.course_create, name = 'create'),
	path('<int:id>/update', views.course_update, name = 'update'),
	path('<int:id>/delete', views.course_delete, name = 'delete'),

]
