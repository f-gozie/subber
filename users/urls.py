from django.urls import path
from django.conf.urls import url

# from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "users"
urlpatterns = [
	# path('api-token-auth/', obtain_auth_token, name='api_auth_token'),
	path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_auth_token'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('create_username/', views.CreateUsernameView.as_view(), name='create_username'),
	path('verify_email/', views.VerifyEmailView.as_view(), name='verify_email'),
	path('resend_otp/', views.ResendOTPView.as_view(), name='resend_otp')
]