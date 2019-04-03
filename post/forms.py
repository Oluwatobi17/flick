from django import forms
from .models import Post, Postcomment

class EditPost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'postType']

class CommentPost(forms.ModelForm):

    class Meta:
        model = Postcomment
        fields = ['body']

class CreateNewPost(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title', 'body', 'postType', 'category']