from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
from .models import Comment

from .forms import CommentForm
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, HttpResponseRedirect

@login_required(login_url='/account/login')
def reply(request, id=None):
	item = get_object_or_404(Comment , id = id)
	content_object = item.content_object
	initial_data = {
		"content_type": item.content_type,
		"object_id" : item.object_id
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
			if parent_qs.exists():
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
				user = request.user,
				content_type= content_type,
				object_id = obj_id,
				content = content,
				parent = parent_obj,

			)
		return redirect("comments:comments", id=item.id)

	#comments = item.comment
	context = {
		"comment" : item,
		
		"form" : form
	}
	return render (request, "reply.html", context)


@login_required(login_url='/account/login')
def delete_comment(request, id=None):
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404
	if obj.user != request.user:
		#messages.success(request, "You do not have permission")
		#raise Http404
		response = HttpResponse("You do not have permission.")
		response.status_code = 403
		return response

	if request.method == 'POST':
		if obj.parent != None:

			obj.delete()
			#messages.success(request, "This has been deleted")
			return redirect("comments:comments", id=obj.parent.id)
		else:
			parent_obj_url = obj.content_object.get_absulte_url()

			
			obj.delete()
			#messages.success(request, "This has been deleted")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object": obj,
	}
	return render(request, "delete_comment.html", context)






























