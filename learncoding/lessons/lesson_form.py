
from django import forms
from pagedown.widgets import PagedownWidget

from .models import Lesson


class LessonCreate(forms.ModelForm):
	
	content = forms.CharField(widget = PagedownWidget)
	class Meta :
		model = Lesson
		fields = [
			"title",
			"content",
			"image",
			"video",

		]