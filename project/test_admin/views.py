from django.shortcuts import render, redirect
from test_maker.models import Test,Question
from user_auth.models import User
import hashlib

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
