from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class TeacherSignUpForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			'establishment',
		]
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_teacher = True
		if commit:
			user.save()
		return user


class StudentSignUpForm(UserCreationForm):
	interests = forms.ModelMultipleChoiceField(
		queryset=Subject.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={'class':'custom-control custom-checkbox'}),
		required=True
	)

	class Meta(UserCreationForm.Meta):
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			'establishment',
			'interests',
		]
	def save(self, commit):
		user = super().save(commit=False)
		user.is_student = True
		user.save()
		student = Student.objects.create(user=user)
		student.interests.add(*self.cleaned_data.get('interests'))
		return user

class StudentProfileUpdateForm(forms.ModelForm):
	interests = forms.ModelMultipleChoiceField(
		queryset=Subject.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True
	)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['interests'].initial = Student.objects.get(user=self.instance).first()
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'establishment',
			'profile_pic',
			'interests',
			'bio'
		]
	def save(self, commit=False):
		user = super().save(commit=False)
		user.save()
		student = Student.objects.get(user=user)
		student.interests.clear()
		student.interests.add(*self.cleaned_data.get('interests'))
		return user

class TeacherProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'establishment',
			'profile_pic',
			'bio'
		]
'''
class QuizzCreateForm(forms.ModelForm):
	questions_text = forms.ModelMultipleChoiceField()
	anwsers_text = forms.ModelMultipleChoiceField()
	class Meta:
		model = Quizz
		fields = [
		'title',
		'subject',
		'author',
		'questions_text',
		'anwsers_text',
		]
	def save(self, commit=False):
		pass
'''