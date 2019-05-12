
from django import forms

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget= forms.PasswordInput)
	
	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This User does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("This User no longer active")
				



	
class RegisterForm(forms.ModelForm):
	email = forms.EmailField(label= "Email Address")
	email2 = forms.EmailField(label = "Confirm Email")
	password = forms.CharField(widget= forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"email2",
			"password"

		]
	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email != email2 :
			raise forms.ValidationError("Email Not Match")
		email_qs = User.objects.filter(email=email)

		if email_qs.exists():
			raise forms.ValidationError("This email already register")


		return email 




















