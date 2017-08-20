from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserProfile, GameSwitch, Building, Question
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import TeamForm, LoginForm, AnswerForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from .controls import calculate_score
from ipware.ip import get_ip


def test(request):
    return HttpResponse('Fack! it is working :D')
    
def index(request):
        return render(request, 'mainapp/index.html',)

def register(request):
    up = UserProfile.objects.filter(ip_address=get_ip)
    if up is None or 1:
        form = TeamForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                data = form.cleaned_data
                u = User()
                u.username = data['teamname']
                u.set_password(data['password'])
                try:
                    u.save()
                except IntegrityError:
                    return HttpResponse('Team name already registered or other conflicting entries')
                up = UserProfile()
                up.user = u
                up.teamname = data['teamname']
                up.name1=data['name1']
                up.name2=data['name2']
                up.phone1 = data['phone1']
                up.phone2 = data['phone2']
                up.email1=data['email1']
                up.email2=data['email2']
                up.id1=data['idno1']
                up.id2=data['idno2']
                up.ip_address = get_ip(request)
                up.save()
                return redirect('login')
            else:
                form=TeamForm(request.POST)
                return render(request,'mainapp/register.html',{'form':form})
        return render(request,'mainapp/register.html',{'form':form})
    else:
        return HttpResponse('You have already registered once from this pc! Contact neartest ACM invigilator')
    

def instructions(request):
    return render(request, 'mainapp/instructions.html')

def login(request):
    g=GameSwitch.objects.get(name='main')
    if g.start_game and not g.end_game:
        lform = LoginForm(request.POST)
        if request.method == 'POST':
            if lform.is_valid():
                data=lform.cleaned_data
                teamname = data['teamname']
                password = data['password']
                user = authenticate(username = teamname, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('game')
            else:
                return HttpResponse('Invalid form')
        else:
            lform=LoginForm(request.POST)
            return render(request, 'mainapp/login.html',{'lform':lform,})
        return render(request, 'mainapp/login.html',{'lform':lform,})
    else:
        return HttpResponse('The game is not started yet, or it has already ended')

def game(request):
    question = Question.objects.all()
    up = UserProfile.objects.get(user=request.user)
    sl= list(up.status)
    up.score=0
    for q in question:
        ch = sl[q.pk-1]
        if ch=='1':
            up.score-=20
        elif ch=='2':
            up.score+=100
        elif ch=='3':
            up.score-=10
    up.save()
    building = Building.objects.all()
    return render(request, 'mainapp/game.html',{'up':up,'question':question})

def question(request,ques_id):
    index = int(ques_id) -1
    up = UserProfile.objects.get(user=request.user)
    q = Question.objects.get(pk=ques_id)
    sl= list(up.status)
    sl[index]="1"
    up.status="".join(sl)
    ansform=AnswerForm(request.POST)
    if request.method == 'POST':
        if ansform.is_valid():
            data=ansform.cleaned_data
            ans= data['answer']
            if ans is not None:
                if q.answer == ans:
                    sl[index]="2"
                    up.status="".join(sl)
                    up.save()
                    return redirect('game')
                else :
                    sl[index]="3"
                    up.status="".join(sl)
                    up.save()
        up.status="".join(sl)
        up.save()   
        return render(request, 'mainapp/questions.html',{'q':q,'ansform':ansform,})
    else:
        ansform=AnswerForm(request.POST)
        return render (request,'mainapp/questions.html',{'q':q,'ansform':ansform,})
