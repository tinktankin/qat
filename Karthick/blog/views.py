from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Blog
from .models import Sing
from .models import Multp
from .models import Ess
from .models import Userr


# Create your views here.

def index(request):
    message = "hello users"
    return render(request,'index1.html',{"msg": message})

def home(request):
    message = "hello users"
    return render(request,'index.html',{"msg": message})

def butt(request):
    return render(request,'butt.html',{})

def but(request):
    return render(request,'but.html',{})

def questionn(request):
    if request.method == "GET":
        return render(request,'questionn.html',{})
    elif request.method == "POST":
        try:
            blog = Blog()
            blog.QuestionBank = request.POST["QuestionBank"]
            blog.category = request.POST["category"]
            blog.typee = request.POST["typee"]
            blog.dur = request.POST["dur"]
            blog.save()
        except:
            return render(request, 'questionn.html',{"msg" : "fill form again"})
        return redirect('blog:test')
def manage(request):
    blog = Blog.objects.all()
    return render(request,'manage.html',{"blog" : blog})

def sc(request):
    return render(request,'sc.html',{})


def nextt(request):
    return render(request,'nextt.html',{})

def single(request):
    if request.method == "GET":
            return render(request,'single.html',{})
    elif request.method == "POST":
        try:
            blog1 = Sing()
            blog1.QQ_1 = request.POST["QQ_1"]
            blog1.op_1 = request.POST["op_1"]
            blog1.op_2 = request.POST["op_2"]
            blog1.op_3 = request.POST["op_3"]
            blog1.save()
        except:
            return render(request, 'single.html',{"msg" : "fill Question again"})
        return redirect('blog:single')

def ques(request):
    blog1 = Sing.objects.all()
    return render(request,'ques.html',{"blog" : blog1})
    

def mul(request):
    if request.method == "GET":
            return render(request,'mul.html',{})
    elif request.method == "POST":
        try:
            blog2 = Multp()
            blog2.Q1 = request.POST["Q1"]
            blog2.a1 = request.POST["a1"]
            blog2.b1 = request.POST["b1"]
            blog2.c1 = request.POST["c1"]
            blog2.d1 = request.POST["d1"]
            blog2.save()
        except:
            return render(request, 'mul.html',{"msg" : "fill Question again"})
        return redirect('blog:test')

def mult(request):
    blog2 = Multp.objects.all()
    return render(request,'mult.html',{"blog" : blog2})

def essay(request):
    if request.method == "GET":
         return render(request,'essay.html',{})
            
    elif request.method == "POST":
        try:
            blog3 = Ess()
            blog3.Q2 = request.POST["Q2"]
            blog3.es = request.POST["es"]
            blog3.save()
        except:
            return render(request, 'essay.html',{"msg" : "fill Question again"})
        return redirect('blog:test')
    

def buttons(request):
    return render(request,'buttons.html',{})

def buttonss(request):
    blog1 = Sing.objects.all()
    return render(request,'buttonss.html',{"blog" : blog1})

def esss(request):
    blog3 = Ess.objects.all()
    return render(request,'esss.html',{"blog" : blog3})

def gallery(request):
    return render(request,'gallery.html',{})


def dropzone(request):
    return render(request,'dropzone.html',{})

def advanced_form_components(request):
    return render(request,'advanced_form_components.html',{})

def basic_table(request):
    blog4 = Userr.objects.all()
    return render(request,'basic_table.html',{"blog" : blog4})

def blank(request):
    return render(request,'blank.html',{})

def chartjs(request):
    return render(request,'chartjs.html',{})

def chat_room(request):
    return render(request,'chat_room.html',{})


def flot_chart(request):
    return render(request,'flot_chart.html',{})


def form_component(request):
    if request.method == "GET":
         return render(request,'form_component.html',{})
            
    elif request.method == "POST":
        try:
            blog4 = Userr()
            blog4.name = request.POST["name"]
            blog4.uname = request.POST["uname"]
            blog4.email = request.POST["email"]
            blog4.psw = request.POST["psw"]
            blog4.cpsw = request.POST["cpsw"]
            blog4.cou = request.POST["cou"]
            blog4.save()
        except:
            return render(request, 'form_component.html',{"msg" : "fill again"})
        return redirect('blog:home')
    


def inbox(request):
    return render(request,'inbox.html',{})


def lobby(request):
    return render(request,'lobby.html',{})


def lock_screen(request):
    return render(request,'lock_screen.html',{})

def login(request):
    return render(request,'login.html',{})

def morris(request):
    return render(request,'morris.html',{})

def profile(request):
    return render(request,'profile.html',{})

def xchart(request):
    return render(request,'xchart.html',{})

def google_maps(request):
    return render(request,'google_maps.html',{})

def test(request):
    return render(request,'test.html',{})

def testm(request):
    return render(request,'testm.html',{})

def testt(request):
    return render(request,'testt.html',{})

def calendarr(request):
    return render(request,'calendarr.html',{})

def pro(request):
    blog4 = Userr.objects.all()
    return render(request,'pro.html',{"blog" : blog4})

def singlq(request):
    blog1 = Sing.objects.all()
    return render(request,'singlq.html',{"blog" : blog1})

def questt(request):
    blog = Blog.objects.all()
    return render(request,'questt.html',{"blog" : blog})
  

