from django import forms
from .models import User, Wall, WallReply, Contact


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username','email', 'password']

class EditProfileForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name','email']

class ProfilePicsForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['profilePics']


class WriteOnWallForm(forms.ModelForm):

	class Meta:
		model = Wall
		fields = ['body']

class WallReplyForm(forms.ModelForm):

	class Meta:
		model = WallReply
		fields = ['body']

class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = ['sender', 'email', 'subject', 'message']