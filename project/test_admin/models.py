from django.db import models

class Questionbank(models.Model):
    name = models.CharField(max_length=1000)
    category = models.CharField(max_length=1000)
    exam_type = models.CharField(max_length=1000)
    visibility = models.CharField(max_length=1000)
    creator = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

class MCQ(models.Model):
    question_bank = models.ForeignKey(Questionbank, on_delete=models.CASCADE)
    ques_type = models.CharField(max_length=1000, default="MCQ", blank=True, null=True)
    ques = models.CharField(max_length=2000)
    op_a = models.CharField(max_length=1000)
    op_b = models.CharField(max_length=1000)
    op_c = models.CharField(max_length=1000)
    op_d = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return "{} - {} - {}".format(self.ques_type,self.ques,self.question_bank.name)

class ManyCorrect(models.Model):
    question_bank = models.ForeignKey(Questionbank, on_delete=models.CASCADE)
    ques_type = models.CharField(max_length=1000, default="ManyCorrect", blank=True, null=True)
    ques = models.CharField(max_length=2000)
    op_a = models.CharField(max_length=1000)
    op_b = models.CharField(max_length=1000)
    op_c = models.CharField(max_length=1000)
    op_d = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return "{} - {} - {}".format(self.ques_type,self.ques,self.question_bank.name)

class OpenAnswer(models.Model):
    question_bank = models.ForeignKey(Questionbank, on_delete=models.CASCADE)
    ques_type = models.CharField(max_length=1000, default="OpenAnswer", blank=True, null=True)
    ques = models.CharField(max_length=2000)
    answer = models.TextField(max_length=50000)

    def __str__(self):
        return "{} - {} - {}".format(self.ques_type,self.ques,self.question_bank.name)