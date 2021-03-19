from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return self.name

class Photo(models.Model):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	image = models.ImageField(null=False, blank=False)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField(max_length=500, null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	tags = TaggableManager()
	#url = models.URLField(default='http://www.foo.com')
	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
		related_name='images_liked',blank=True)

	def __str__(self):
		return '{}, {}, {}, {}'.format(self.category, self.image, self.created, self.description)

	def get_absolute_url(self):
		return reverse('gallery')

class Comment(models.Model):
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE,
		related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	image = models.ImageField(null=False, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return f'Comment by {self.name} on {self.photo}'

	class Meta:
		ordering = ('created',)