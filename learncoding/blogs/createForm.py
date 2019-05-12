

from django import forms
from pagedown.widgets import PagedownWidget

from .models import Blog


class PostCreate(forms.ModelForm):
	publish = forms.DateField(widget= forms.SelectDateWidget)
	content = forms.CharField(widget = PagedownWidget)
	class Meta :
		model = Blog
		fields = [
			"title",
			"content",
			"publish",
			"draf",
			"image",

		]