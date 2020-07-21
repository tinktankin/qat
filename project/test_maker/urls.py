from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "test_maker"

urlpatterns = [
	path('', views.test, name='test'),
	path('ques/', views.ques, name='ques'),
	path('addmcq/', views.add_mcq, name='add_mcq'),
	path('addopen/', views.add_open, name='add_open'),
	path('preview/',views.preview, name ='preview'),
	path('CreateTest/',views.create_test, name='create_test'),
	path('viewall/',views.view_all, name='view_all'),
	path('view_test/<str:name>',views.view_test, name='view_test'),
	path('selectadmin/<str:name>',views.select, name='select_admin'),
	path('students_enrolled/',views.student, name='student'),
]