from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import Http404, HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from .tokens import account_activation_token
from .forms import *
from .models import User, Subject
import json

def is_teacher(user):
	'''for the user passes test decorator'''
	return user.is_teacher

def is_takenquizz_owner(view_func):
	def decorator(request, *args, **kwargs):
		pk = kwargs["pk"]
		taken_quizz = get_object_or_404(TakenQuizz, pk=pk)
		if not (taken_quizz.user.id == request.user.id):
			return HttpResponse("You can't see this quizz results", status = 403)
		return view_func(request, *args, **kwargs)
	return decorator

def SignupView(request, usertype):
	if request.user.is_authenticated:
		return redirect('private-profile')
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
	if request.user.is_authenticated:
		return redirect('private-profile')
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		checkuser = User.objects.get(username=username)
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

@login_required
def LogoutView(request):
	logout(request)
	messages.success('You are logged out.')
	return redirect('home')

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

@login_required
def ChangePasswordView(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'auth/change_password.html', {
		'form': form
	})

@login_required
@user_passes_test(is_teacher, )
def CreateQuizzView(request):
	if request.POST:
		data = request.POST
		quizzname = data['quizzname']
		subject = data['subject']
		questions
	else:
		subjects = Subject.objects.all()
		return render(request, 'create-quizz.html',{'subjects':subjects})

@csrf_exempt
@login_required
def PassQuizzView(request, pk):
	quizz = get_object_or_404(Quizz,pk = pk)
	questions = Question.objects.filter(quizz = quizz)
	if request.POST:
		i = 0
		total_score = 0
		user_score = 0
		for question in questions:
			answers = Answer.objects.filter(question = question, is_correct = True).values_list('text', flat = True)
			total_score += len(answers)
			user_answers = request.POST[f'answer{i}[]']
			# for answr in user_answers:
				# print("answr:",answr)
			if user_answers in list(answers):
				user_score +=1
			i += 1
		taken_quizz = TakenQuizz.objects.create(quizz = quizz, user = request.user, score = (user_score*100)/total_score )

		return redirect(f'/quizz/taken/{taken_quizz.pk}')
	else:
		data = {'quizzname': quizz.title,'subject':quizz.subject.name,'author':quizz.author.username,'questions':[]}
		for question in questions:
			question_text = question.text
			answers = Answer.objects.filter(question = question).values_list('text', flat = True)
			data['questions'].append({'question':question_text, "options" : list(answers)})

		return render(request, 'pass-quizz.html', { 'data' : json.dumps(data) })

@login_required
@is_takenquizz_owner
def TakenQuizzView(request, pk):
	taken_quizz = get_object_or_404(TakenQuizz, pk = pk)
	quizz = get_object_or_404(Quizz, pk = taken_quizz.quizz.pk)
	questions = Question.objects.filter(quizz = quizz)
	data = {'questions':[]}
	for question in questions:
		question_text = question.text
		answers = Answer.objects.filter(question = question).values_list('text', flat = True)
		correct_answers = Answer.objects.filter(question = question, is_correct = True).values_list('text', flat = True)
		data['questions'].append({'question':question_text,"answers":list(correct_answers)})

	return render(request, 'result-quizz.html', {'taken_quizz' : taken_quizz, 'data':data})

