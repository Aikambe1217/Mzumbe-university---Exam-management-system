from django.urls import path
from . import views

urlpatterns = [

	path('index', views.index, name = 'index'),
    path('collection', views.collection, name = 'collection'),
    path('submission', views.submission, name = 'submission'),
    path('return_page', views.return_page, name = 'return_page'),
	path('report', views.report, name = 'report'),
    path('submission_records', views.submission_records, name = 'submission_records'),
    path('collection_records', views.collection_records, name = 'collection_records'),
    path('return_records', views.return_records, name = 'return_records'),
    path('edit_submission_record', views.edit_submission_record, name='edit_submission_record'),
    # path('delete_record', views.delete_record, name='delete_record'),

    path('profile', views.profile, name = 'profile'),
    

   
	
	

]