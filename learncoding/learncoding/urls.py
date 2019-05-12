"""learncoding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from courses.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name = 'home'),

    path('account/', include("account.urls", namespace = "account")),
    path('blogs/', include("blogs.urls", namespace = "blogs")),
    path('courses/', include("courses.urls", namespace = "courses")),
    path('courses/', include("lessons.urls", namespace = "lessons")),
    path('comment/', include("comments.urls", namespace = "comment")),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
