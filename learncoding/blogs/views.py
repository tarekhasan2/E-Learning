from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required

from .models import Blog
from urllib.parse import quote_plus
from django.db.models import Q
from django.core.paginator import Paginator
from .createForm import PostCreate
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from django.http import HttpResponse, HttpResponseRedirect, Http404

def postHome(request):
	queryset = Blog.objects.all()
	query = request.GET.get("q")
	if query:
		queryset = queryset.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)
			).distinct()

	paginator = Paginator(queryset, 3) # Show 25 contacts per pag

	page = request.GET.get('page')
	contents = paginator.get_page(page)
	context= {
		"titel": "All blog Post",
		"queryset" : contents,
		
		
	}
	return render (request, "postHome.html", context)



def postDetails(request, id=None):
	item = get_object_or_404(Blog , id = id)

	share_string = quote_plus(item.content)
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
		"share_string" : share_string,
		"comments" :comments,
		"form" : form
	}
	return render (request, "postDetails.html", context)



@login_required(login_url='/account/login')
def postCreate(request):
	if request.user.is_staff or request.user.is_superuser:
		form = PostCreate(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Seccessfully Created")
			return HttpResponseRedirect(instance.get_absulte_url())
		context = {
			"form":form
		}

		return render (request, "postCreate.html", context)
	else:
		raise Http404


@login_required(login_url='/account/login')
def postUpdate(request, id=None):
	if request.user.is_staff or request.user.is_superuser:

		instance = get_object_or_404(Blog, id=id)
		form = PostCreate(request.POST or None, request.FILES or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Seccessfully Edited")
			return HttpResponseRedirect(instance.get_absulte_url())
		context = {
			"instance":instance,
			"form":form
		}

		return render (request, "postUpdate.html", context)
	else:
		raise Http404

@login_required(login_url='/account/login')
def postDelete(request, id=None):
	if request.user.is_staff or request.user.is_superuser:

		item = get_object_or_404(Blog, id = id)
		if request.POST:
			item.delete()
			return redirect('blogs:list') 
		context= {
			"item":item,

		}
		return render (request, "postDelete.html", context)
	else:
		raise Http404
