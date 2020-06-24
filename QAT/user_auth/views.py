from django.shortcuts import render, redirect
import hashlib
from .models import User


def check_user_exists(request, email):
    if request is None:
        return (None, None)
    for u in User.objects.all():
        if hashlib.sha256(str(u.email).encode()).hexdigest() == email:
            return (True, u)            
    return (False, None)

# Create your views here.
def signup(request):
    if request.method=='GET':
        if request.session.has_key('username'):
            return redirect('user_auth:home')
        else:
            return render(request, 'user_auth/Login_Registration.html', {'status': 0})
    elif request.method=='POST':
        if "email" in request.POST and "password" in request.POST and "Retype_password" in request.POST:
            v, u = check_user_exists(request, hashlib.sha256(str(request.POST['email']).encode()).hexdigest())
            if not v:
                if request.POST["password"] == request.POST["Retype_password"]:
                    if len(request.POST['phone_no']) == 10:
                        password = hashlib.sha256(str(request.POST['password']).encode()).hexdigest()
                        user = User(email=request.POST["email"], password=password, first_name=request.POST["name"], username=request.POST["username"], phone_no=request.POST["phone_no"], gender=request.POST["gender"])
                        if(request.POST["user_type"]=="Test Taker"):
                            print("Testtaker")
                            user.user_type = 'TESTTAKER'
                        elif(request.POST["user_type"]=="Test Maker"):
                            print("Testsetter")
                            user.user_type = 'TESTMAKER'
                        elif(request.POST["user_type"]=="Test Admin"):
                            print('testadmin')
                            user.user_type = 'TESTADMIN'
                        print("1")
                        user.save()
                        print("1")
                        return render(request, 'user_auth/Login_Registration.html')
                    else:
                        return render(request, 'user_auth/Login_Registration.html', {'warning': 'The phone number should be 10 numbers only'})
                else:
                    return render(request, 'user_auth/Login_Registration.html', {'warning': 'The password should match'})
            else:
                return render(request, 'user_auth/Login_Registration.html', {'warning': 'User already exists'})
        else:
            return render(request, 'user_auth/Login_Registration.html', {'warning': 'Fill all the details as'})

def login(request):
    if request.method == 'GET':
        if request.session.has_key('username'):
            return redirect('user_auth:home')
        else:
            return render(request, 'user_auth/Login_Registration.html', {'status': 1})
    elif request.method == 'POST':
        if "email" in request.POST and "password" in request.POST:
            v,user = check_user_exists(request, hashlib.sha256(str(request.POST['email']).encode()).hexdigest())
            if v:
                password = hashlib.sha256(str(request.POST['password']).encode()).hexdigest()
                if password == user.password:
                    request.session['username'] = hashlib.sha256(str(user.email).encode()).hexdigest()
                    if user.user_type == "Test Taker":
                        request.session['status'] = 0
                    elif user.user_type == "Test Maker":
                        request.session['status'] = 1
                    elif user.user_type == 'Test Admin':
                        request.session['status'] = 2
                    return home(request)
                else:
                    return render(request, 'user_auth/Login_Registration.html', {'warning': 'Enter the correct password'})
            else:
                return render(request, 'user_auth/Login_Registration.html', {'warning': 'User does not exists'})
        else:
            return render(request, 'user_auth/Login_Registration.html', {'warning': 'Enter all the fields'})

def home(request):
    login_status=0
    if request.session.has_key('username'):
        v,user = check_user_exists(request, request.session['username'])
        if v:
            login_status = 1
            return render(request, 'user_auth/home.html', {'user': user, 'user_type': user.user_type, 'login_status': login_status})
        else:
            return render(request, 'user_auth/home.html', {'warning': 'Permission denied'})
    else:
        return render(request, 'user_auth/home.html', {'login_status': login_status})
    

def logout(request):
    if request.session.has_key('username'):
        print(request.session['username'])
        if check_user_exists(request, request.session['username'])[0]:
            request.session.flush()
        else:
            return render(request, 'user_auth/home.html', {'warning': 'Permission denied'})
    return redirect('user_auth:home')

def oauth(request):
    return redirect('user_auth:home')