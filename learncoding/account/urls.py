
from django.contrib import admin
from django.urls import path


from . import views
app_name = "account"

urlpatterns = [

	path('login', views.login_view, name= 'login'),
	path('register', views.register_view, name= 'register'),
	path('logout', views.logout_view, name= 'logout'),
	#path('comments/<int:id>/delete', views.comment_delete, name = 'delete'),


]

