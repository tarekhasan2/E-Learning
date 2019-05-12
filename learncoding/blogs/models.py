from django.db import models
from comments.models import Comment
from django.urls import reverse
from markdown_deux import markdown
from django.contrib.contenttypes.models import ContentType

from django.utils.safestring import mark_safe
# Create your models here


class Blog(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	image = models.FileField(null=True, blank=True)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	draf = models.BooleanField(default=False)
	
	class Meta:
		ordering = ["-publish"]


	def __str__(self):
		return self.title


	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)


	def get_absulte_url(self):
		return reverse("blogs:details" ,kwargs={"id":self.id})


	@property
	
	def comment(self):
		item = self
		qs = Comment.objects.filter_by_instence(item = item)
		return qs

	def get_content_type(self):
		item = self
		content_type = ContentType.objects.get_for_model(item.__class__)
		return content_type

		

