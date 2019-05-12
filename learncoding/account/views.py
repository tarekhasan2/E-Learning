from django.shortcuts import render, redirect, reverse

from .forms import LoginForm, RegisterForm
# Create your views here.

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

def login_view(request):
	form = LoginForm(request.POST or None)
	next = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect ("/blogs/posts")


	context ={
		"form" : form

	}
	return render (request, "log_view.html", context) 



def register_view(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.is_staff = True
		user.save()
		return redirect ("/account/login")
	context = {
		"form" :form
	}
	return render (request, "log_view.html", context)


def logout_view(request):
	logout(request)
	context = {

	}
	return redirect("/account/login")