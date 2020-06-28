from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    USER_CHOICES = (
      ('TESTTAKER', 'testtaker'),
      ('TESTMAKER', 'testmaker'),
      ('TESTADMIN', 'testadmin'),
      ('ADMIN', 'admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_CHOICES)
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    gender = models.CharField(max_length=20, choices=GENDERS)
    phone_no = models.IntegerField(null = True)
    organisation = models.CharField(max_length=30, null=True)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    date_of_birth = models.DateField(null=True)
    email_verified = models.BooleanField(default=False)