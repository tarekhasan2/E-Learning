from django.contrib import admin

# Register your models here.

from .models import Course

class BlogModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Course

admin.site.register(Course, BlogModelAdmin)