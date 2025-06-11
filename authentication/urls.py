from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

	path('', views.login, name = 'login'),
	path('register', views.register, name = 'register'),
	path('admin_auth', views.admin_auth, name = 'admin_auth'),
	path('logout',views.logout, name = 'logout'),
    path('clear-preloader-session/', views.clear_preloader_session, name='clear_preloader_session'),
    
	
	# email......
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/password_reset_form.html',
             email_template_name='password_reset/password_reset_email.html',
             subject_template_name='password_reset/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]