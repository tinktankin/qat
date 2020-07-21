from django.contrib import admin
from . import models

admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.CreateTest)
admin.site.register(models.Testadmin)
admin.site.register(models.StudentList)