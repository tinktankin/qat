from django.shortcuts import render, redirect
from test_maker.models import Test,Question
from user_auth.models import User
import hashlib
from .models import Questionbank,MCQ,ManyCorrect,OpenAnswer

def get_user(request,email):
    if request is None:
        return None
    for u in User.objects.all():
            if hashlib.sha256(str(u.email).encode()).hexdigest() == email:
                return u
    return None

def test(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			if request.method == 'GET':
				org = u.organisation
				available_test = []
				for test in Test.objects.all():
					if test.organisation == org:
						available_test.append(test)
				return render(request, 'test_admin/test.html',{"test":available_test})
			return redirect('user_auth:home')
		return redirect('user_auth:home')


def ques(request,exam):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			try:
				test = Test.objects.get(exam_name = exam)
				ques = Question.objects.filter(test_rel = test)
			except:
				return redirect('user_auth:home')

			if request.method == "GET":
				return render(request, "test_admin/ques.html", {"obj": test,"ques":ques})
			else:
				ques_type = request.POST["ques_type"]
				print(ques_type,type(ques_type))
				if ques_type == "1":
					return redirect(f"../../{exam}/addmcq/")
				elif ques_type == "2":
					return redirect(f"../../{exam}/addopen/")
				else:
					return render(request, "test_admin/ques.html", {"obj": test,"ques":ques})
		return redirect('user_auth:home')
	return redirect('user_auth:home')


def add_mcq(request,exam):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			try:
				test = Test.objects.get(exam_name = exam)
			except:
				return redirect('user_auth:home')

			if request.method == "GET":
				return render(request,"test_admin/add_mcq.html")
			else:
				ques = Question(
					ques_type = 1,
					question = request.POST["question"],
					option_a = request.POST["option_a"],
					option_b = request.POST["option_b"],
					option_c = request.POST["option_c"],
					option_d = request.POST["option_d"],
					ans = int(request.POST["ques_ans"]),
					max_marks = request.POST["max_marks"],
					min_marks = request.POST["min_marks"],
				)
				try:
					ques.save()
					ques.test_rel.add(test)
				except:
					return render(request,"test_admin/add_mcq.html",{"msg":"Fill Form Correctly"})
				return redirect(f"../../ques/{exam}")
		return redirect('user_auth:home')
	return redirect('user_auth:home')
		

def add_open(request,exam):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			try:
				test = Test.objects.get(exam_name = exam)
			except:
				return redirect('user_auth:home')

			if request.method == "GET":
				return render(request,"test_admin/add_open.html")
			else:
				ques = Question(
					ques_type = 2,
					question = request.POST["question"],
					correct_write_ans = request.POST["correct_ans"],
					ans = 5,
					max_marks = request.POST["max_marks"],
					min_marks = request.POST["min_marks"],
				)
				try:
					ques.save()
					ques.test_rel.add(test) 
				except:
					return render(request,"test_admin/add_open.html",{"msg":"Fill Form Correctly"})
				return redirect(f"../../ques/{exam}")
		return redirect('user_auth:home')	
	return redirect('user_auth:home')


def preview(request,exam):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			try:
				test = Test.objects.get(exam_name = exam)
				ques = Question.objects.filter(test_rel = test)
			except:
				return redirect('user_auth:home')
		return render(request, "test_admin/preview.html", {"obj": test,"ques":ques})

	return redirect('user_auth:home')


def create_qbank(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		if u.user_type == 'TESTADMIN':
			if request.method == 'GET':
				return render(request,'test_admin/add_qbank.html',{})
			elif request.method == 'POST':
				try:
					obj = Questionbank()
					obj.name = request.POST["name"]
					obj.category = request.POST["category"]
					obj.exam_type = request.POST["exam_type"]
					obj.visibility = request.POST["visibility"]
					obj.creator = u.username
					obj.save()
					return redirect('test_admin:ManageQBank',obj.name)
				except:
					msg = "Error, Try Again !!"
					return render(request,'test_admin/add_qbank.html',{"msg":msg})
	return redirect('user_auth:home')

def manage(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		mcq = list(MCQ.objects.filter(question_bank=obj))
		manycorrect = list(ManyCorrect.objects.filter(question_bank=obj))
		openques = list(OpenAnswer.objects.filter(question_bank=obj))
		all_ques = []
		all_ques.extend(mcq)
		all_ques.extend(manycorrect)
		all_ques.extend(openques)
		return render(request,'test_admin/manage.html',{"QBank":obj, "questions":all_ques})
	return redirect('user_auth:home')

def AddMcq(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		if request.method == 'GET':
			return render(request,'test_admin/mcq.html',{"QBank":obj})
		elif request.method == 'POST':
			mcq = MCQ()
			mcq.question_bank = obj
			mcq.ques = request.POST["ques"]
			mcq.op_a = request.POST["op_a"]
			mcq.op_b = request.POST["op_b"]
			mcq.op_c = request.POST["op_c"]
			mcq.op_d = request.POST["op_d"]
			mcq.answer = request.POST["answer"]
			mcq.save()
			return redirect('test_admin:ManageQBank',obj.name)
	return redirect('user_auth:home')

def AddMultiple(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		if request.method == 'GET':
			return render(request,'test_admin/multiple.html',{"QBank":obj})
		elif request.method == 'POST':
			many = ManyCorrect()
			many.question_bank = obj
			many.ques = request.POST["ques"]
			many.op_a = request.POST["op_a"]
			many.op_b = request.POST["op_b"]
			many.op_c = request.POST["op_c"]
			many.op_d = request.POST["op_d"]
			many.answer = request.POST.getlist("answer")
			print(request.POST.getlist("answer"))
			many.save()
			return redirect('test_admin:ManageQBank',obj.name)
	return redirect('user_auth:home')

def AddOpen(request, name):
		if request.session.has_key('username'):
			logged_in = request.session['username']
			u = get_user(request,logged_in)
			obj = Questionbank.objects.filter(name=name)[0]
			if request.method == 'GET':
				return render(request,'test_admin/open.html',{"QBank":obj})
			elif request.method == 'POST':
				op = OpenAnswer()
				op.question_bank = obj
				op.ques = request.POST["ques"]
				op.answer = request.POST["answer"]
				print(request.POST["answer"])
				op.save()
				return redirect('test_admin:ManageQBank',obj.name)
		return redirect('user_auth:home')


def ViewMcq(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		all_mcq = MCQ.objects.filter(question_bank=obj)
		return render(request,'test_admin/view_multiple.html',{
			"all_mcq":all_mcq,
			"obj" : obj,
		})
	return redirect('user_auth:home')

def ViewOpen(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		all_open = OpenAnswer.objects.filter(question_bank=obj)
		return render(request,'test_admin/view_essay.html',{
			"all_open":all_open,
			"obj" : obj,
		})
	return redirect('user_auth:home')

def ViewMultiple(request, name):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		obj = Questionbank.objects.filter(name=name)[0]
		all_many = ManyCorrect.objects.filter(question_bank=obj)
		return render(request,'test_admin/view_single.html',{
			"all_many":all_many,
			"obj" : obj,
		})
	return redirect('user_auth:home')


def manage_qbank(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		query = Questionbank.objects.filter(creator=u.username)
		return render(request, 'test_admin/manage_qbank.html', {"obj":query})
	return redirect('user_auth:home')


def all_ques(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		u = get_user(request,logged_in)
		query = Questionbank.objects.filter(creator=u.username)
		all_ques = []
		for i in query:
			mcq = list(MCQ.objects.filter(question_bank=i))
			manycorrect = list(ManyCorrect.objects.filter(question_bank=i))
			openques = list(OpenAnswer.objects.filter(question_bank=i))
			all_ques.extend(mcq)
			all_ques.extend(manycorrect)
			all_ques.extend(openques)
		return render(request, 'test_admin/all_ques.html', {"questions":all_ques})
	return redirect('user_auth:home')