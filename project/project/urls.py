from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_auth.urls')),
    path('testadmin/', include('test_admin.urls')),
    path('testmaker/', include('test_maker.urls')),
    # path('accounts/', include('allauth.urls')),
]
