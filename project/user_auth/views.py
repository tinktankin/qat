from django.shortcuts import render, redirect
import hashlib
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.http import HttpResponse
from test_admin.models import Questionbank,MCQ,ManyCorrect,OpenAnswer,Test
from .models import User,StudentResponse
from .tokens import account_activation_token
from random import shuffle
from datetime import datetime,timedelta

# Checks whether user exists and returns user value
def check_user_exists(request, email):
    if request is None:
        return (None, None)
    for u in User.objects.all():
        if hashlib.sha256(str(u.email).encode()).hexdigest() == email:
            return (True, u)            
    return (False, None)

def get_user(request,email):
    if request is None:
        return None
    for u in User.objects.all():
            if hashlib.sha256(str(u.email).encode()).hexdigest() == email:
                return u
    return None

# Signup for users.
def signup(request):
    if request.method=='GET':
        # If user already logged in
        if request.session.has_key('username'):
            return redirect('user_auth:home')
        # If user not logged in render signup template
        else:
            return render(request, 'user_auth/Login_Registration.html', {'status': 0})
    elif request.method=='POST':
        if "email" in request.POST and "password" in request.POST and "Retype_password" in request.POST:
            # Check whether user already exists
            v, u = check_user_exists(request, hashlib.sha256(str(request.POST['email']).encode()).hexdigest())
            if not v:
                if request.POST["password"] == request.POST["Retype_password"]:
                    if len(request.POST['phone_no']) == 10:
                        # Encrypting password
                        password = hashlib.sha256(str(request.POST['password']).encode()).hexdigest()
                        user = User(email=request.POST["email"], password=password, first_name=request.POST["name"], username=request.POST["username"], phone_no=request.POST["phone_no"], gender=request.POST["gender"])
                        # Based on the usertype store in the database
                        if(request.POST["user_type"]=="Test Taker"):
                            print("Testtaker")
                            user.user_type = 'TESTTAKER'
                        elif(request.POST["user_type"]=="Test Maker"):
                            print("Testsetter")
                            user.user_type = 'TESTMAKER'
                            user.organisation = request.POST["organisation"]
                        elif(request.POST["user_type"]=="Test Admin"):
                            print('testadmin')
                            user.user_type = 'TESTADMIN'
                            user.organisation = request.POST["organisation"]
                        # Save user
                        user.gender = str(request.POST["gender"]).capitalize()
                        print(str(request.POST["gender"]).capitalize())
                        user.save()
                        request.session['username'] = hashlib.sha256(str(user.email).encode()).hexdigest()
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your account.'
                        message = render_to_string('user_auth/activmail.html', {
                        'username': user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.username)).decode(),
                        'token': account_activation_token.make_token(user),
                        })
                        # to_email = user.email
                        # email = EmailMessage(
                        #     mail_subject, message, to=[to_email]
                        # )
                        # email.send()
                        return redirect('user_auth:login')
                    else:
                        return render(request, 'user_auth/Login_Registration.html', {'warning': 'The phone number should be 10 numbers only'})
                else:
                    return render(request, 'user_auth/Login_Registration.html', {'warning': 'The password should match'})
            else:
                return render(request, 'user_auth/Login_Registration.html', {'warning': 'User already exists'})
        else:
            return render(request, 'user_auth/Login_Registration.html', {'warning': 'Fill all the details as'})

# Login for users
def login(request):
    if request.method == 'GET':
        # If user is already logged in
        if request.session.has_key('username'):
            return redirect('user_auth:home')
        # If user not logged in render login template
        else:
            return render(request, 'user_auth/Login_Registration.html', {'status': 1})
    elif request.method == 'POST':
        if "email" in request.POST and "password" in request.POST:
            # Check whether user exists
            v,user = check_user_exists(request, hashlib.sha256(str(request.POST['email']).encode()).hexdigest())
            if v:
                password = hashlib.sha256(str(request.POST['password']).encode()).hexdigest()
                # Validation of password
                if password == user.password:
                    request.session['username'] = hashlib.sha256(str(user.email).encode()).hexdigest()
                    if user.user_type == 'TESTTAKER':
                        request.session['status'] = 0
                    elif user.user_type == 'TESTMAKER':
                        request.session['status'] = 1
                    elif user.user_type == 'TESTADMIN':
                        request.session['status'] = 2
                    return redirect('user_auth:home')
                else:
                    return render(request, 'user_auth/Login_Registration.html', {'warning': 'Enter the correct password'})
            else:
                return render(request, 'user_auth/Login_Registration.html', {'warning': 'User does not exists'})
        else:
            return render(request, 'user_auth/Login_Registration.html', {'warning': 'Enter all the fields'})

# Home page
def home(request):
    login_status=0
    # Check if user is logged in
    if request.session.has_key('username'):
        # Check whether user exists
        v,user = check_user_exists(request, request.session['username'])
        if v:
            login_status = 1
            return render(request, 'user_auth/home.html', {'user': user, 'user_type': user.user_type, 'login_status': login_status})
        else:
            return render(request, 'user_auth/home.html', {'warning': 'Permission denied'})
    else:
        return redirect('user_auth:login')
        # return render(request, 'user_auth/home.html', {'login_status': login_status})
    
# Logout for users
def logout(request):
    # Check if user is logged in
    if request.session.has_key('username'):
        print(request.session['username'])
        if check_user_exists(request, request.session['username'])[0]:
            request.session.flush()
        else:
            return render(request, 'user_auth/home.html', {'warning': 'Permission denied'})
    return redirect('user_auth:login')

# Social authentication
# def oauth(request):
#     return redirect('user_auth:home')

# Activate account by email verification
def activate(request, uidb64, token):
    try:
        # Decode the user
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(username = uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    # Check whether token is correct
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect('user_auth:home')
    else:
        return HttpResponse('user_auth:login')


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'user_auth/forgot_password.html')
    elif request.method == 'POST':
        v, u = check_user_exists(request, hashlib.sha256(str(request.POST['email']).encode()).hexdigest())
        if v:
            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            message = render_to_string('user_auth/forgot_password_email.html', {
            'username': u.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(u.username)).decode(),
            'token': account_activation_token.make_token(u),
            })
            to_email = u.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'user_auth/forgot_password.html', {'message': 'Email has been sent to ' + to_email})


def display_save_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(username = uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        a = hashlib.sha256(str(user.email).encode()).hexdigest()
        return render(request, 'user_auth/save_password.html', {'a': a})
    else:
        return HttpResponse('Activation link is invalid!')

def save_password(request):
    if request.method == 'POST':
        v, user = check_user_exists(request, request.POST['id'])
        password = request.POST['password']
        retype_password = request.POST['retype_password']
        if password == retype_password:
            user.password = hashlib.sha256(str(password).encode()).hexdigest()
            user.save()
            return redirect('user_auth:home')
        else:
            return HttpResponse('Both passwords should match')


def profile(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request, logged_in)
        return render(request, 'user_auth/Profile.html', {"user" : u})
    return redirect('user_auth:login')

def test_exam(request, name):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request, logged_in)
        obj = Test.objects.get(name=name)
        mcq = list(MCQ.objects.filter(test=obj))
        manycorrect = list(ManyCorrect.objects.filter(test=obj))
        openques = list(OpenAnswer.objects.filter(test=obj))
        all_ques = []
        all_ques.extend(mcq)
        all_ques.extend(manycorrect)
        all_ques.extend(openques)
        n = len(all_ques)
        shuffle(all_ques)
        try:
            ls = StudentResponse.objects.filter(test=obj)
            for i in ls:
                if i.student == u.username:
                    return HttpResponse('Test already taken by you')
        except:
            print("Taking Test")   
        if request.method=='GET':
            return render(request,'user_auth/main.html',{"questions":(all_ques),"obj":obj,"n":n,"user":u})
        else:
            for ques in all_ques:
                response = StudentResponse()
                response.test = obj
                response.student = u.username
                response.ques_type = ques.ques_type
                response.ques = ques.ques
                if ques.ques_type == 'MCQ':
                    ans = request.POST.get('{}'.format(ques.ques))
                    response.op_a = ques.op_a
                    response.op_b = ques.op_b
                    response.op_c = ques.op_c
                    response.op_d = ques.op_d
                if ques.ques_type == 'ManyCorrect':
                    ans = request.POST.getlist('{}'.format(ques.ques))
                    response.op_a = ques.op_a
                    response.op_b = ques.op_b
                    response.op_c = ques.op_c
                    response.op_d = ques.op_d
                if ques.ques_type == 'OpenAnswer':
                    ans = request.POST.get('{}'.format(ques.ques))
                print(ans)
                response.submission_time = datetime.now().time()
                response.answer = ques.answer
                response.marks = ques.marks
                response.negative_marks = ques.negative_marks
                response.student_answer = ans
                response.save()
            return redirect('user_auth:home')
    return redirect('user_auth:home')

def view_all(request):
    if request.session.has_key('username'):
        logged_in = request.session['username']
        u = get_user(request,logged_in)
        all_test = Test.objects.all()
        tests = []
        for test in all_test:
            if test.date == datetime.now().date() and (test.time <= datetime.now().time() <= (datetime.now()+timedelta(minutes=test.duration)).time()):
                tests.append((test,True))
            else:
                tests.append((test,False))
        return render(request, 'user_auth/view_all.html',{"all_test":tests[::-1]})
    return redirect('user_auth:home')