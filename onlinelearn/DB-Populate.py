import json 
from classroom.models import (Question, Answer,Quizz, Subject, User)

with open('questions-dataset.json','r') as f:
	data = json.load(f)
	f.close()

sub = Subject.objects.filter(name= 'General Knowledge').first()
user = User.objects.filter(username='fa2y').first()
quizz = Quizz.objects.create( title = 'test_quizz', subject = sub, author = user)

for question in data['questions']:
	index = 0
	qst = Question.objects.create(text = question['question'], quizz = quizz)
	for answr in question['answers']:
		answer = Answer.objects.create(question = qst, text = answr)
		if index == question['correctIndex']:
			answer.is_correct = True
			answer.save()
		index += 1
