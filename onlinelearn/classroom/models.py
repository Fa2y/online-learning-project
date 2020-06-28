from django.db import models
from django.contrib.auth.models import AbstractUser

def wrapperuser(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('images/', filename)

class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)
	establishment = models.CharField(max_length=50)
	bio = models.CharField(max_length=400)
	profile_pic = models.ImageField(upload_to=wrapperuser, default="default.jpg")

	def __str__(self):
		return self.username

class Subject(models.Model):
	name = models.CharField(max_length=15)
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Quizz(models.Model):
	title = models.CharField(max_length=50)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Student(models.Model):
	user= models.OneToOneField(User, on_delete=models.CASCADE)
	interests = models.ManyToManyField(Subject)
	quizzez = models.ManyToManyField(Quizz)

	def __str__(self):
		return self.user.username

class Question(models.Model):
	text = models.CharField(max_length=200)
	quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=100)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.text

class TakenQuizz(models.Model):
	quizz = models.ForeignKey(Quizz, on_delete=models.SET_NULL, null=True)
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
	score = models.FloatField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.quizz.title+' resuls for '+self.student.__str__

#It needs further development, we leave like that for now
class Course(models.Model):
	title = models.CharField(max_length=60)
	content = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)
