# Generated by Django 2.1 on 2020-06-30 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques_type', models.PositiveSmallIntegerField(choices=[(1, 'Multiple Choice'), (2, 'Open Answer')], default=1)),
                ('question', models.CharField(max_length=1000, null=True)),
                ('option_a', models.CharField(blank=True, max_length=20, null=True)),
                ('option_b', models.CharField(blank=True, max_length=20, null=True)),
                ('option_c', models.CharField(blank=True, max_length=20, null=True)),
                ('option_d', models.CharField(blank=True, max_length=20, null=True)),
                ('correct_write_ans', models.TextField(blank=True, max_length=3000, null=True)),
                ('ans', models.PositiveSmallIntegerField(choices=[(1, models.CharField(blank=True, max_length=20, null=True)), (2, models.CharField(blank=True, max_length=20, null=True)), (3, models.CharField(blank=True, max_length=20, null=True)), (4, models.CharField(blank=True, max_length=20, null=True)), (5, models.TextField(blank=True, max_length=3000, null=True))], default=1)),
                ('max_marks', models.IntegerField(default=5)),
                ('min_marks', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=30)),
                ('exam_date', models.DateField(default=datetime.date.today)),
                ('exam_time', models.TimeField(null=True)),
                ('user', models.CharField(blank=True, max_length=40)),
                ('organisation', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test_rel',
            field=models.ManyToManyField(to='test_maker.Test'),
        ),
    ]