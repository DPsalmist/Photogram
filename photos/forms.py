from django import forms
from .models import Photo, Comment

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ('category','image','description','tags',)
		#exclude = ['owner', 'tags', 'users_like',]

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body',)
