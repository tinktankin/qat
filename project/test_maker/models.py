from django.db import models
import datetime


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
