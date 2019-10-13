from django.contrib import admin
from .models import Content
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.


class ContentAdmin(admin.ModelAdmin):

	fieldsets = [("Title/Date", {"fields": ["content_title", "content_published"]}),
	("Content", {"fields": ["content_content"]})]

	formfield_overrides = {models.TextField: {'widget': TinyMCE()}}


admin.site.register(Content, ContentAdmin)