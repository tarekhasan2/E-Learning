from django.contrib import admin

# Register your models here.

from .models import Blog

class BlogModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Blog

admin.site.register(Blog, BlogModelAdmin)