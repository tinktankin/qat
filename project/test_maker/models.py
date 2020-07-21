from django.db import models
import datetime
from user_auth.models import User


class Test(models.Model):
	exam_name = models.CharField(max_length=30)
	exam_date = models.DateField(default=datetime.date.today)
	exam_time = models.TimeField(null = True)
	user = models.CharField(max_length=40, blank=True)
	organisation = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return self.exam_name


class Question(models.Model):
	question_type = (
			(1,"Multiple Choice"),
			(2,"Open Answer"),
		)
	test_rel = models.ManyToManyField(Test)
	ques_type = models.PositiveSmallIntegerField(choices=question_type, default=1) 
	question = models.CharField(max_length=1000, null=True)
	option_a = models.CharField(max_length=20, null=True, blank=True )
	option_b = models.CharField(max_length=20, null=True, blank=True)
	option_c = models.CharField(max_length=20, null=True, blank=True)
	option_d = models.CharField(max_length=20, null=True, blank=True)
	correct_write_ans = models.TextField(max_length=3000, null=True, blank=True)
	ans_possiblities = (
		(1,option_a),
		(2,option_b),
		(3,option_c),
		(4,option_d),
		(5,correct_write_ans),
	)
	ans = models.PositiveSmallIntegerField(choices = ans_possiblities, default=1)
	max_marks = models.IntegerField(default=5)
	min_marks = models.IntegerField(default=0,blank=True)

	def __str__(self):
		if self.ques_type == 1:
			q_type = "MCQ"
		else:
			q_type = "OPEN ANSWER"
		return f"{q_type} = {self.question}"

class CreateTest(models.Model):
	publisher = models.CharField(max_length=1000)
	name = models.CharField(max_length=1000)
	category = models.CharField(max_length=1000)
	date = models.DateField(default=datetime.date.today)
	time = models.TimeField(null = True)
	duration = models.IntegerField()
	negative = models.BooleanField()
	creator = models.CharField(max_length=500)
	organisation = models.CharField(max_length=500, blank=True)

	def __str__(self):
		return "{} - {}".format(self.name, self.publisher)

class Testadmin(models.Model):
	test = models.ForeignKey(CreateTest, on_delete=models.CASCADE)
	admin = models.CharField(max_length=5000)

	def __str__(self):
		return "Admins - {}".format(self.test)

class StudentList(models.Model):
	test = models.ForeignKey(CreateTest, on_delete=models.CASCADE, unique=True)
	user = models.ManyToManyField(User)

	def __str__(self):
		return "Student - {}".format(self.test)

