from django import forms
from datetime import datetime


class ReportForm(forms.Form):
	your_name = forms.CharField(required=True)
	your_email = forms.EmailField(required=True)
	date_time_of_incident= forms.DateTimeField(initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=False)    
	description = forms.CharField(required=True, widget=forms.Textarea)