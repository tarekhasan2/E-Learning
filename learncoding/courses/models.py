from django.db import models
from django.conf import settings
# Create your models here.
from django.urls import reverse
from comments.models import Comment

from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType


def uploded_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Course(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=True)
	title = models.CharField(max_length=120)
	content = models.TextField()
	image = models.ImageField(upload_to = uploded_location, null=True, blank=True)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	video = models.FileField(upload_to = uploded_location, null=True, blank=True)



	class Meta:
		ordering = ["-publish"]



	def __unicode__(self):
		return str(self.title)

	def __str__(self):
		return self.title


	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)


	@property

	def comment(self):
		item = self
		qs = Comment.objects.filter_by_instence(item = item)
		return qs


	def get_content_type(self):
		item = self
		content_type = ContentType.objects.get_for_model(item.__class__)
		return content_type

		

	def get_absulte_url(self):
		return reverse("courses:details" , kwargs={"id":self.id})