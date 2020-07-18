from django.db import models

class Blog(models.Model):
    QuestionBank = models.TextField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    typee = models.CharField(max_length=200)
    dur = models.CharField(max_length=200)

    def __str__(self):
        return self.QuestionBank
        return self.typee

class Sing(models.Model):
    QQ_1 = models.TextField(max_length=200, unique=True)
    op_1 = models.TextField(max_length=200, unique=True)
    op_2 = models.TextField(max_length=200, unique=True)
    op_3 = models.TextField(max_length=200, unique=True)

    def __str__(self):
        return self.QQ_1

class Multp(models.Model):
    Q1 = models.TextField(max_length=200, unique=True)
    a1 = models.TextField(max_length=200, unique=True)
    b1 = models.TextField(max_length=200, unique=True)
    c1 = models.TextField(max_length=200, unique=True)
    d1 = models.TextField(max_length=200, unique=True)

    def __str__(self):
        return self.Q1

class Ess(models.Model):
    Q2 = models.TextField(max_length=200, unique=True)
    es = models.TextField(max_length=200, unique=True)

    def __str__(self):
        return self.Q2


class Userr(models.Model):
    name = models.TextField(max_length=200, unique=True)
    uname = models.TextField(max_length=200, unique=True)
    email = models.TextField(max_length=200, unique=True)
    psw = models.TextField(max_length=200, unique=True)
    cpsw = models.TextField(max_length=200, unique=True)
    cou = models.TextField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name



        






