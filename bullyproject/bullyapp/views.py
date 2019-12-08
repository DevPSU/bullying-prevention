from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Content, User, Report
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .forms import StudentRegisterForm, TeacherRegisterForm, ReportForm
from django.contrib.auth.decorators import login_required
from .decorators import student_required, teacher_required
from django.views.generic import CreateView
from django.db import connection


# Can view, does not require login
def homepage(request):
	return render(request = request,
				  template_name='main/home.html',
				  context = {"content":Content.objects.all})

##This displays page where user gets to choose student or teacher
def register(request):
	return render(request = request,
					template_name = "main/register.html")

def profile(request):
    return render(request = request,
                  template_name="main/profile.html",)

def reports(request):
    # return render_to_response('index.html')
    return render(request=request,
                  template_name="index.html",
				  context={'report':Report.objects.all}
                  )

class StudentRegisterView(CreateView):
	model = User
	form_class = StudentRegisterForm
	template_name = 'main/register _form.html'

	#This method is used to populate a dictionary to use as the template context.
	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		username = form.cleaned_data.get('username')
		messages.success(self.request, f"New account created: {username}")
		login(self.request, user)
		messages.info(self.request, f"You are now logged in as {username}")
		return redirect("main:homepage")
		
class TeacherRegisterView(CreateView):
	model = User
	form_class = TeacherRegisterForm
	template_name = 'main/register _form.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'teacher'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		username = form.cleaned_data.get('username')
		messages.success(self.request, f"New account created: {username}")
		login(self.request, user)
		messages.info(self.request, f"You are now logged in as {username}")
		return redirect("main:homepage")


def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
			
	form = AuthenticationForm()
	connection.close()
	return render(request = request,
					template_name = "main/login.html",
					context={"form":form})
	

# Can view when both types users are logged in
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:homepage")

def report(request):

	model = Report
	form_class = ReportForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get(
				'your_name'
			, '')
			contact_email = request.POST.get(
				'your_email'
			, '')
			location = request.POST.get(
				'location'
			, '')
			datetime = request.POST.get('date_time_of_incident', '')
			form_description = request.POST.get('description', '')

			template = get_template('main/report_template.txt')

			context = {
				'contact_name': contact_name,
				'contact_email': contact_email,
				'location': location,
				'datetime': datetime,
				'form_description': form_description,
			}
			content = template.render(context)

			email = EmailMessage(
				"New contact form submission",
				content,
				"Your website" +'',
				['youremail@gmail.com'],
				headers = {'Reply-To': contact_email }
			)
			email.send()
			report = form.save()
			messages.info(request, f"Your report is sent.")
			connection.close()

	return render(request, 'main/report.html', {
		'form': form_class,
	})

#only students can view 
#@login_required
#@student_required  # <-- use decorator functions here to secify that only students can view!

#use this if your using class based views
#@method_decorator([login_required, student_required], name='dispatch')



#only teachers can view 
