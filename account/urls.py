from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	# Accounts URLS
	#path('login/', views.user_login, name='login'),
	path('logout/', views.logoutUser, name='logout'),
	path('login/', auth_views.LoginView.as_view(), name='login'), 
	path('register/', views.register, name='register'),
	path('profile/', views.edit, name='edit'),
	path('', views.dashboard, name='dashboard'),

	# Change password urls
   path('password_change/', auth_views.PasswordChangeView.as_view( 
   	template_name='account/password_change_form.html'), name='password_change'),
   path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
   	template_name='account/password_change_done.html'), name='password_change_done'),

   #Password reset urls
   path('password_reset/', auth_views.PasswordResetView.as_view(
   	template_name='account/password_reset_form.html'), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
   	template_name='account/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
   	template_name='account/password_reset_confirm.html'),name='password_reset_confirm'),
   path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
   	template_name='account/password_reset_complete.html'),name='password_reset_complete'),

]