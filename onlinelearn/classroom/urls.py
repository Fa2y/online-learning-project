from django.conf.urls import url
from classroom import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^signup/$', views.SignupView, name='signup' ),
	url(r'^signup/(?P<usertype>.*)/$', views.SignupView, name='signup' ),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		views.ActivateView, name='activate'),
	url(r'^login/', views.LoginView, name='login'),
	url(r'^logout/', views.LogoutView, name='logout'),
	url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.ProfileView, name='profile'),
	url(r'^account/profile', views.PrivateProfileView, name='private-profile'),
	url(r'^account/changepassword/$', views.ChangePasswordView, name='change-password'),
	url(r'^quizz/create$',views.CreateQuizzView, name='create-quizz'),
	url(r'^quizz/create/(?P<quizzid>[0-9]+)$',views.QuizzAddQstView, name='create-quizz-add-qst'),
	url(r'^quizz/create/complete/(?P<quizzid>[0-9]+)$',views.QuizzCompleteView, name='create-quizz-complete'),
	url(r'^quizz/(?P<pk>[0-9]+)$',views.PassQuizzView, name='pass-quizz'),
	url(r'^quizz/taken/(?P<pk>[0-9]+)$',views.TakenQuizzView, name='result-quizz'),
	url(r'^$', views.HomeView, name='home'),
#.....setting up static route like this just for debugging 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)