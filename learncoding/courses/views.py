from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Course
from django.core.paginator import Paginator
from comments.models import Comment
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lessons.models import Lesson
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .course_form import CourseCreate




def Home(request):
	query_set = Course.objects.all()
	count = 0
	query_list = []
	for x in query_set:
		query_list.append(x)
		count += 1
		if count==3:
			break
	query1 = query_list[0]
	query2 = query_list[1]
	query3 = query_list[2]
	context ={
		"query1" : query1,
		"query2" : query2,
		"query3" : query3
	}

	return render (request, "home.html" , context)


def courses(request):
	query_set = Course.objects.all()



	paginator = Paginator(query_set, 2) # Show 25 contacts per pag

	page = request.GET.get('page')
	contents = paginator.get_page(page)
	context={
		"query_set" :contents,
	
	}

	return render (request, "courses.html", context)



def course_details(request, id=None):
	item = get_object_or_404(Course , id = id)

	#share_string = quote_plus(item.content)
	lessons = Lesson.objects.filter(parent = id)

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
		"lessons": lessons,
		"comments" :comments,
		"form" : form
		#"share_string" : share_string
	}
	return render (request, "course_details.html", context)



@login_required(login_url='/account/login')
def course_create(request):
	if request.user.is_staff or request.user.is_superuser :

		form = CourseCreate(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Seccessfully Created")
			return HttpResponseRedirect(instance.get_absulte_url())
		context = {
			"form":form
		}
		return render (request, "course_create.html", context)
	else:
		raise Http404

@login_required(login_url='/account/login')
def course_update(request, id=None):
	if request.user.is_staff or request.user.is_superuser :

		instance = get_object_or_404(Course, id=id)
		form = CourseCreate(request.POST or None, request.FILES or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False, )
			instance.user = request.user
			instance.save()
			messages.success(request, "Seccessfully Edited")
			return HttpResponseRedirect(instance.get_absulte_url())
		context = {
			"form":form
		}

		return render (request, "course_update.html", context)
	else:
		raise Http404


@login_required(login_url='/account/login')
def course_delete(request, id=None):
	if request.user.is_staff or request.user.is_superuser :

		item = get_object_or_404(Course , id=id)
		if request.POST:
			item.delete()

			return redirect("courses:list")
		context = {
			"item":item
		}
		return render (request, "course_delete.html")
	else:
		raise Http404




		
	