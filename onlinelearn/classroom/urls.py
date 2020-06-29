from django.conf.urls import url
from classroom import views


urlpatterns = [
	url(r'^signup/(?P<usertype>.*)', views.StudentSignupView, name='student-signup' ),
	url(r'signup/teacher', views.TeacherSignupView, name='teacher-signup' ),
	 url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]