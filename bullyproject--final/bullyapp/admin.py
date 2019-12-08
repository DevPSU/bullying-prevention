from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import Content, User, Report

# Register your models here.

class ReportAdmin(admin.ModelAdmin):

	fieldsets = [("Name and Email", {"fields": ['your_name', 'your_email']}), 
	("Information", {"fields": ["location", "date_time_of_incident", 'description']})]
	
admin.site.register(Report, ReportAdmin)



class UserAdmin(admin.ModelAdmin):

	fieldsets = [("Name", {"fields": ['first_name', 'last_name']}), 
	("Information", {"fields": ["username", "password"]})]

admin.site.register(User, UserAdmin)


class ContentAdmin(admin.ModelAdmin):

	fieldsets = [("Title/Date", {"fields": ["content_title", "content_published"]}),
	("Content", {"fields": ["content_content"]})]

	formfield_overrides = {models.TextField: {'widget': TinyMCE()}}


admin.site.register(Content, ContentAdmin)

