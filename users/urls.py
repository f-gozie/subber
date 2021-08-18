from django.urls import path
from django.conf.urls import url

from . import views

app_name = "users"
urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('create_username/', views.CreateUsernameView.as_view(), name='create_username')
]