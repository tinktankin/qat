from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from test_admin.models import Test

class User(AbstractUser):
    USER_CHOICES = (
      ('TESTTAKER', 'testtaker'),
      ('TESTMAKER', 'testmaker'),
      ('TESTADMIN', 'testadmin'),
      ('ADMIN', 'admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_CHOICES)
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    gender = models.CharField(max_length=20, choices=GENDERS)
    phone_no = models.IntegerField(null = True)
    organisation = models.CharField(max_length=30, null=True)
    email_verified = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    date_of_birth = models.DateField(null=True)

class StudentResponse(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.CharField(max_length=1000)
    ques_type = models.CharField(max_length=100)
    ques = models.CharField(max_length=5000)
    op_a = models.CharField(max_length=1000,null=True,blank=True)
    op_b = models.CharField(max_length=1000,null=True,blank=True)
    op_c = models.CharField(max_length=1000,null=True,blank=True)
    op_d = models.CharField(max_length=1000,null=True,blank=True)
    answer = models.CharField(max_length=1000)
    submission_time = models.TimeField()
    marks = models.IntegerField(default=10, null=True, blank=True)
    negative_marks = models.IntegerField(default=0, blank=True, null=True)
    student_answer = models.CharField(max_length=1000)

    def __str__(self):
        return self.student