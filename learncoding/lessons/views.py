from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Lesson
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

from django.http import HttpResponse, HttpResponseRedirect

from .lesson_form import LessonCreate



def lesson_create(request, id = None):
	form = LessonCreate(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.parent = id
		instance.save()
		messages.success(request, "Seccessfully Created")
		return HttpResponseRedirect(instance.get_absulte_url())
	context = {
		"form":form
	}

	return render (request, "course_create.html", context)


def lesson_details(request, id=None):
	item = get_object_or_404(Lesson , id = id)

	#share_string = quote_plus(item.content)
	initial_data = {
		"content_type": item.get_content_type,
		"object_id" : item.id
	}

	form = CommentForm(request.POST or None , initial =initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs:
				parent_obj= parent_qs

		new_comment, created = Comment.objects.get_or_create(
				user = request.user,
				content_type= content_type,
				object_id = obj_id,
				content = content,
				parent = parent_obj

			)
		return HttpResponseRedirect(new_comment.content_object.get_absulte_url())

	comments = item.comment
	
	context = {
		"item" : item,
		"comments" :comments,
		"form" : form
		#"share_string" : share_string
	}
	return render (request, "lesson_details.html", context)


@login_required(login_url='/account/login')
def lesson_update(request, id=None):
	instance = get_object_or_404(Lesson, id=id)
	form = LessonCreate(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False, )
		instance.user = request.user
		instance.save()
		messages.success(request, "Seccessfully Edited")
		return HttpResponseRedirect(instance.get_absulte_url())
	context = {
		"form":form
	}

	return render (request, "course_create.html", context)


@login_required(login_url='/account/login')
def lesson_delete(request, id=None):

	item = get_object_or_404(Lesson , id=id)

	if request.POST:
		item.delete()

		return redirect("courses:details" , id = item.parent)
	context = {
		"item":item
	}
	return render (request, "course_delete.html", context)
	