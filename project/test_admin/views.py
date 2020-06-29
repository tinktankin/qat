from django.shortcuts import render, redirect
from .models import Test,Question


def test(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		if request.method == 'GET':
			return render(request, 'test_admin/test.html')
		else:
			test = Test(
				exam_name = request.POST["exam_name"],
				exam_date = request.POST["exam_date"],
				exam_time = request.POST["exam_time"],
				user = logged_in,
			)
			try:
				test.save()
			except:
				return render(request, 'test_admin/test.html',{"msg":"fill the form correctly"})	
			return redirect("/test/ques/")
	return redirect('user_auth:home')


def ques(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		try:
			test = Test.objects.get(user = logged_in)
			ques = Question.objects.filter(test_rel = test)
		except:
			return redirect('user_auth:home')

		if request.method == "GET":
			return render(request, "test_admin/ques.html", {"obj": test,"ques":ques})
		else:
			ques_type = request.POST["ques_type"]
			print(ques_type,type(ques_type))
			if ques_type == "1":
				return redirect("test_admin:add_mcq")
			elif ques_type == "2":
				return redirect("test_admin:add_open")
			else:
				return render(request, "test_admin/ques.html", {"obj": test,"ques":ques})
	return redirect('user_auth:home')


def add_mcq(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		print(logged_in)
		test = Test.objects.get(user = logged_in)
		if request.method == "GET":
			return render(request,"test_admin/add_mcq.html")
		else:
			ques = Question(
				test_rel = test,
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
			except:
				return render(request,"test_admin/add_mcq.html",{"msg":"Fill Form Correctly"})
			return redirect("test_admin:ques")

	return redirect('user_auth:home')
	

def add_open(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		test = Test.objects.get(user = logged_in)
		if request.method == "GET":
			return render(request,"test_admin/add_open.html")
		else:
			ques = Question(
				test_rel = test,
				ques_type = 2,
				question = request.POST["question"],
				correct_write_ans = request.POST["correct_ans"],
				ans = 5,
				max_marks = request.POST["max_marks"],
				min_marks = request.POST["min_marks"],
			)
			try:
				ques.save()
			except:
				return render(request,"test_admin/add_open.html",{"msg":"Fill Form Correctly"})
			return redirect("test_admin:ques")
			
	return redirect('user_auth:home')


def preview(request):
	if request.session.has_key('username'):
		logged_in = request.session['username']
		try:
			test = Test.objects.get(user = logged_in)
			ques = Question.objects.filter(test_rel = test)
		except:
			return redirect('user_auth:home')
		return render(request, "test_admin/preview.html", {"obj": test,"ques":ques})

	return redirect('user_auth:home')
