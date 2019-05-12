from django.db import models
from django.conf import settings
# Create your models here.
from django.urls import reverse
#from django.utils.safestring import mark_safe

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CommentManager(models.Manager):
	def filter_by_instence(self, item):
		content_type = ContentType.objects.get_for_model(item.__class__)
		object_id = item.id
		qs = super(CommentManager, self).filter(content_type=content_type, object_id= object_id, parent=None)
		return qs






class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
	objects = CommentManager()

	class Meta:
		ordering = ["-timestamp"]

	def __unicode__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("comments:comments", kwargs={"id":self.id})

	def get_delete_url(self):
		return reverse("comments:delete_comment", kwargs={"id":self.id})


	def children(self):
		return Comment.objects.filter(parent=self)


