from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Content
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import ReportForm
from django.template.loader import get_template
from django.core.mail import EmailMessage


def homepage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context = {"content":Content.objects.all})


def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:homepage")

		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")

	form = UserCreationForm
	return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
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
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})


def profile(request):
    return render(request = request,
                  template_name="main/profile.html",)


def reports(request):
    # return render_to_response('index.html')
    return render(request=request,
                  template_name="index.html",
                  )

def report(request):

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
            datetime = request.POST.get('date_time_of_incident', '')
            form_description = request.POST.get('description', '')

            template = get_template('main/report_template.txt')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
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

    return render(request, 'main/report.html', {
        'form': form_class,
    })