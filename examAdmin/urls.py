from django.urls import path
from . import views
from .views import toggle_staff_status

urlpatterns = [

 path('dashboard', views.dashboard, name = 'dashboard'),
 path('collections', views.collections, name = 'collections'),
 path('marked', views.marked, name = 'marked'),
 path('profile', views.profile, name = 'profile'),
 path('reports', views.reports, name = 'reports'),
 path('system_settings', views.system_settings, name = 'system_settings'),
 path('submissions', views.submissions, name = 'submissions'),
 path('users', views.users, name = 'users'),
 path('toggle-staff-status/', views.toggle_staff_status, name='toggle_staff_status'),
 path('backup/', views.backup_database, name='backup_database'),
 path('delete_submitted_item/<int:pk>/', views.delete_submitted_item, name='delete_submitted_item'),
 path('delete_collected_item/<int:pk>/', views.delete_collected_item, name='delete_collected_item'),
 path('delete_returned_item/<int:pk>/', views.delete_returned_item, name='delete_returned_item'),
 path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
 path('addsubmission', views.addsubmission, name = 'addsubmission'),
 path('addcollection', views.addcollection, name = 'addcollection'),
 path('addmarked', views.addmarked, name = 'addmarked'),
 path('edit_submission_record', views.edit_submission_record, name='edit_submission_record'),




]