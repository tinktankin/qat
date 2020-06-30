from django.shortcuts import render, redirect
from .models import Test,Question
import hashlib
# import sys
# sys.path.append("..")
# from ..user_auth.models import User
from user_auth.models import User



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
        print(u)
        if u.user_type == 'TESTMAKER':
            if request.method == 'GET':
                return render(request, 'test_maker/test.html')
            else:
                test = Test(
                    exam_name = request.POST["exam_name"],
                    exam_date = request.POST["exam_date"],
                    exam_time = request.POST["exam_time"],
                    user = logged_in,
                    organisation = u.organisation,
                )
                try:
                    # print(logged_in,u.organisation)
                    test.save()
                except:
                    return render(request, 'test_maker/test.html',{"msg":"fill the form correctly"})	
                return redirect("test_maker:ques")
        return redirect('user_auth:home')
    return redirect('user_auth:home')


def ques(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request,logged_in)
        if u.user_type == 'TESTMAKER':
            try:
                test = Test.objects.get(user = logged_in)
                ques = Question.objects.filter(test_rel = test)
            except:
                return redirect('user_auth:home')

            if request.method == "GET":
                return render(request, "test_maker/ques.html", {"obj": test,"ques":ques})
            else:
                ques_type = request.POST["ques_type"]
                print(ques_type,type(ques_type))
                if ques_type == "1":
                    return redirect("test_maker:add_mcq")
                elif ques_type == "2":
                    return redirect("test_maker:add_open")
                else:
                    return render(request, "test_maker/ques.html", {"obj": test,"ques":ques})
        return redirect('user_auth:home')
    return redirect('user_auth:home')


def add_mcq(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request,logged_in)
        if u.user_type == 'TESTMAKER':
            test = Test.objects.get(user = logged_in)
            if request.method == "GET":
                return render(request,"test_maker/add_mcq.html")
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
                    return render(request,"test_maker/add_mcq.html",{"msg":"Fill Form Correctly"})
                return redirect("test_maker:ques")
        return redirect('user_auth:home')
    return redirect('user_auth:home')
	

def add_open(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request,logged_in)
        if u.user_type == 'TESTMAKER':
            test = Test.objects.get(user = logged_in)
            if request.method == "GET":
                return render(request,"test_maker/add_open.html")
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
                    return render(request,"test_maker/add_open.html",{"msg":"Fill Form Correctly"})
                return redirect("test_maker:ques")
        return redirect('user_auth:home')	
    return redirect('user_auth:home')


def preview(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request,logged_in)
        if u.user_type == 'TESTMAKER':
            try:
                test = Test.objects.get(user = logged_in)
                ques = Question.objects.filter(test_rel = test)
            except:
                return redirect('user_auth:home')
            return render(request, "test_maker/preview.html", {"obj": test,"ques":ques})
        return redirect('user_auth:home')
    return redirect('user_auth:home')
