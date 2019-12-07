from django import forms
from django.db import models
from datetime import datetime
from .models import User, Report
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


#Add feature where email and name are not required when logged in.
class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['your_name', 'your_email', 'date_time_of_incident', 'location', 'description']


class StudentRegisterForm(UserCreationForm):

	# What is this?
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username']

    #Help saves data
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user

class TeacherRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username']

        # What is commit?
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
