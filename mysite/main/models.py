from django.db import models
from datetime import datetime

# Create your models here.
class Content(models.Model):
	content_title = models.CharField(max_length = 200)
	content_content = models.TextField()
	content_published = models.DateTimeField("date published", default = datetime.now())

	def __str__(self):
		return self.content_title
