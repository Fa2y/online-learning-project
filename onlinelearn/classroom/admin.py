from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Quizz)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TakenQuizz)
admin.site.register(Course)