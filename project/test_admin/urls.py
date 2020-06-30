from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "test_admin"

urlpatterns = [
	path('', views.test, name='test'),
	path('ques/<str:exam>/', views.ques, name='ques'),
	path('<str:exam>/addmcq/', views.add_mcq, name='add_mcq'),
	path('<str:exam>/addopen/', views.add_open, name='add_open'),
	path('<str:exam>/preview/',views.preview, name ='preview')
]