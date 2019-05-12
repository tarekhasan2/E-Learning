

from django import forms
from pagedown.widgets import PagedownWidget

from .models import Course


class CourseCreate(forms.ModelForm):
	publish = forms.DateField(widget= forms.SelectDateWidget)
	content = forms.CharField(widget = PagedownWidget)
	class Meta :
		model = Course
		fields = [
			"title",
			"content",
			"publish",
			"image",
			"video",

		]
		