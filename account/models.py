from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
	gender = (
			('select', 'select'),
			('male', 'male'),
			('female','female')
		)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	level = models.CharField(max_length=200, blank=True, default=100)
	photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, default='static/photos/media/default.jpeg')
	gender = models.CharField(max_length=100, choices=gender, default='select')
	department = models.CharField(max_length=200, blank=True)
	matric_no = models.CharField(max_length=100, blank=True, unique=True, null=False)
	verified_student = models.BooleanField(default=False)
	
	def __str__(self):
		return f'Profile for user {self.user.username}'