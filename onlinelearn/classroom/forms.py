from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (User, Student, Subject)

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
		widget=forms.CheckboxSelectMultiple,
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
	def save(self):
		user = super().save(commit=False)
		user.is_student = True
		user.save()
		student = Student.objects.create(user=user)
		student.interests.add(*self.cleaned_data.get('interests'))
		return user