from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = "user_auth"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('save_password/', views.save_password, name='save_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    re_path(r'^display_save_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.display_save_password, name='display_save_password'),
    # path('oauth/', views.oauth, name='oauth'),
    path('profile/',views.profile, name='profile'),
    path('test/<str:name>',views.test_exam, name='test'),
    path('all_test/',views.view_all, name='all_test')
]