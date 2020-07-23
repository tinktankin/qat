from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "test_admin"

urlpatterns = [
	# path('', views.test, name='test'),
	# path('ques/<str:exam>/', views.ques, name='ques'),
	# path('<str:exam>/addmcq/', views.add_mcq, name='add_mcq'),
	# path('<str:exam>/addopen/', views.add_open, name='add_open'),
	# path('<str:exam>/preview/',views.preview, name ='preview'),
	path('create-Qbank/',views.create_qbank,name='CreateQBank'),
	path('manage/<str:name>',views.manage, name='ManageQBank'),
	path('addmcq/<str:name>',views.AddMcq, name='AddMcq'),
	path('addmultiple/<str:name>',views.AddMultiple, name='AddMultiple'),
	path('addopen/<str:name>',views.AddOpen, name='AddOpen'),
	path('viewmcq/<str:name>',views.ViewMcq, name='ViewMcq'),
	path('viewmultiple/<str:name>',views.ViewMultiple, name='ViewMultiple'),
	path('viewopen/<str:name>',views.ViewOpen, name='ViewOpen'),
	path('manageq_bank',views.manage_qbank, name='manage_qbank'),
	path('viewques/',views.all_ques, name='viewallques'),
	path('assigned_test/',views.assigned, name='assigned_test'),
	path('manage_test/<str:name>',views.manage_test, name='manage_test'),
	path('addmcqtest/<str:name>',views.AddMcqTest, name='AddMcqTest'),
	path('addmultipletest/<str:name>',views.AddMultipleTest, name='AddMultipleTest'),
	path('addopentest/<str:name>',views.AddOpenTest, name='AddOpenTest'),
	path('add_question_from_bank/<str:name>',views.add_question_from_bank, name='add_question_from_bank'),
]