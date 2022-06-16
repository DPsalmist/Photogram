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
	price = models.CharField(max_length=200, blank=True, default=100)
	transaction_id = models.CharField(max_length=100, null=True)
	tags = TaggableManager()
	#url = models.URLField(default='http://www.foo.com')
	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
		related_name='images_liked',blank=True)

	def __str__(self):
		return '{}, {}, {}, {}'.format(self.category, self.image, self.created, self.description)

	def get_absolute_url(self):
		return reverse('gallery')


# Guest Users Orders
'''
class GuestOrder(models.Model):
    ORDER_STATUS = (
            ('Pending','Pending'),
			('Unapproved','Unapproved'),
			('Delivered','Delivered')
	)
    guest_customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='unregistered_students')
    product = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.CharField(max_length=30, choices=ORDER_STATUS, default='Pending')
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
    	return (f'str({self.id}), str({self.product}), str({self.guest_customer})')
'''

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