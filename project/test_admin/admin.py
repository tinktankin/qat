from django.contrib import admin
from .models import Questionbank,MCQ,ManyCorrect,OpenAnswer,Test

admin.site.register(Questionbank)
admin.site.register(MCQ)
admin.site.register(ManyCorrect)
admin.site.register(OpenAnswer)
admin.site.register(Test)