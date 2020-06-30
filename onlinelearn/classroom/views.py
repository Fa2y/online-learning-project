from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import Http404
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from .forms import *
from .models import User


def SignupView(request, usertype):
	if usertype != 'student' and usertype != 'teacher':
		raise Http404("Unvalid type of user. Only teacher/student are valid.")
	if request.method == 'POST':
		if usertype == 'student':
			form = StudentSignUpForm(request.POST)
		else:
			form = TeacherSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			site = get_current_site(request)
			subject = 'Activate Your OnlineLearn Account'
			message = render_to_string('auth/account_activation_email.html', {
				'user': user,
				'domain': site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			messages.success(request, 'Sign Up successful, Check your email to confirm')
			return redirect('login')
	else:
		if usertype == 'student':
			form = StudentSignUpForm()
		else:
			form = TeacherSignUpForm()

	return render(request, 'auth/signup.html', {"form":form})

def ActivateView(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('home')
	else:
		return redirect('login')


def LoginView(request):
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		checkuser = User.objects.filter(username=username).first()
		if checkuser is not None:
			if not checkuser.email_confirmed:
				messages.error(request, 'Confirm your email to login')
				return render(request, 'auth/login.html',{'username': username})
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Invalid Credentials.')
	return render(request, 'auth/login.html',{'username': username})

def ProfileView(request, username):
	user = get_object_or_404(User, username=username)
	if user.is_active:
		return render(request, 'profile.html', {'user': user})
	raise Http404('User is not active')

@login_required
def PrivateProfileView(request):
	if request.method == 'POST':
		if request.user.is_teacher:
			form = TeacherProfileUpdateForm(request.POST, request.FILES, instance = request.user)
		else:
			form = StudentProfileUpdateForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile updated successfully.')
			return redirect('private-profile')
	else:
		if request.user.is_teacher:
			form = TeacherProfileUpdateForm(instance = request.user)
		else:
			form = StudentProfileUpdateForm(instance = request.user)

		return render(request, 'private-profile.html', {"form":form})