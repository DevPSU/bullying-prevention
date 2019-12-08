from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class Report(models.Model):
	your_name = models.CharField(max_length = 200)
	location = models.CharField(max_length = 200)
	your_email = models.EmailField(max_length = 200)
	date_time_of_incident= models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    
	description = models.TextField()

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class UsernameData(models.Model):
	psuStudentUsername = models.CharField(max_length = 200)
	psuTeacherUsername = models.CharField(max_length = 200)

class Content(models.Model):
	content_title = models.CharField(max_length = 200)
	content_content = models.TextField()
	content_published = models.DateTimeField("date published", default = datetime.now())

	def __str__(self):
		return self.content_title
