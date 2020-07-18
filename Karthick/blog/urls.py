from django.urls import path, re_path, include
from . import views

app_name= "blog"
urlpatterns = [
    path('',views.index,name='index'),
    path('index/test',views.test,name='test'),
    path('test/pro',views.pro,name='pro'),
    path('test/questionn/',views.questionn,name='questionn'),
    path('test/questt/',views.questt,name='questt'),
    path('questt/nextt/',views.nextt,name='nextt'),
    path('test/single/',views.single,name='single'),
    path('test/buttons/',views.buttons,name='buttons'),
    path('buttons/buttonss/',views.buttonss,name='buttonss'),
    path('index/testm',views.testm,name='testm'),
    path('index/testt',views.testt,name='testt'),
    path('testt/calendarr',views.calendarr,name='calendarr'),
    path('but/',views.but,name='but'),
    path('but/index',views.home,name='home'),
    path('index/gallery',views.gallery,name='gallery'),
    path('index/dropzone',views.dropzone,name='dropzone'),
    path('index/advanced_form_components',views.advanced_form_components,name='advanced_form_components'),
    path('index/basic_table',views.basic_table,name='basic_table'),
    path('index/blank',views.blank,name='blank'),
    path('index/chartjs',views.chartjs,name='chartjs'),
    path('index/chat_room',views.chat_room,name='chat_room'),
    path('index/flot_chart',views.flot_chart,name='flot_chart'),
    path('index/form_component',views.form_component,name='form_component'),
    path('index/inbox',views.inbox,name='inbox'),
    path('index/lobby',views.lobby,name='lobby'),
    path('index/lock_screen',views.lock_screen,name='lock_screen'),
    path('index/login',views.login,name='login'),
    path('index/morris',views.morris,name='morris'),
    path('index/profile',views.profile,name='profile'),
    path('index/xchart',views.xchart,name='xchart'),
    path('index/google_maps',views.google_maps,name='google_maps'),
    path('butt/manage/',views.manage,name='manage'),
    path('test/singlq/',views.singlq,name='singlq'),
    path('butt/sc/',views.sc,name='sc'),
    path('butt/mul/',views.mul,name='mul'),
    path('butt/essay/',views.essay,name='essay'),
    path('single/ques/',views.ques,name='ques'),
    path('but/mult/',views.mult,name='mult'),
    path('but/esss/',views.esss,name='esss'),
    

]



