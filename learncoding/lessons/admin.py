from django.contrib import admin

# Register your models here.

from .models import Lesson

class BlogModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Lesson

admin.site.register(Lesson, BlogModelAdmin)