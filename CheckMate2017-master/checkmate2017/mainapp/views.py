from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserProfile, GameSwitch, Building, Question
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import TeamForm, LoginForm, AnswerForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from .controls import calculate_score
from ipware.ip import get_ip
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required


def test(request):
    return HttpResponse('Fack! it is working :D')
    
def index(request):
    #if not request.user.is_authenticated or request.user is 'admin':
        return render(request, 'mainapp/index.html',)
    #else:
        #return redirect('game')

def register(request):
    up = UserProfile.objects.filter(ip_address=get_ip)
    if up is None or 1:#this is for developement time being
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
                return HttpResponse("Failed! Invalid login attempt, make sure that you used your own BITS mail and id!")
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
                    return redirect(reverse('mainapp:game'))
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
    bs= list(up.build_solved)
    up.score=0
    for q in question:
        ch = sl[q.pk-1]
        if ch=='2':
            up.score+=100
    up.score-= (up.wrong_responses*25)
    #up.score-= (up.skipped*10)
    buildings = Building.objects.all()
    for b in buildings:
        bs[b.pk-1]='0'
        qe=Question.objects.filter(building_context=b)
        for qi in qe:
            if sl[qi.pk-1]=='2':
                bs[b.pk-1]=(int(bs[b.pk-1])+1).__str__()

    up.build_solved="".join(bs)
    up.save()
    return render(request, 'mainapp/game.html',{'up':up,'bs':bs,'buildings':buildings})

def question(request,ques_id):
    index = int(ques_id) -1
    up = UserProfile.objects.get(user=request.user)
    q = Question.objects.get(pk=ques_id)
    sl= list(up.status)
    if sl[index]=="2":
        return redirect('game')
    else:
        sl[index]="1"
        up.status="".join(sl)
        ansform=AnswerForm(request.POST)
        if request.method == 'POST':
            if ansform.is_valid():
                data=ansform.cleaned_data
                ans= data['answer']
                if ans is not None:
                    if q.answer == (ans.lower()).strip():
                        sl[index]="2"
                        up.status="".join(sl)
                        up.save()
                        return redirect('game')
                    else :
                        sl[index]="3"
                        up.status="".join(sl)
                        up.wrong_responses+=1
                        up.save()
            if sl[index]== "1":
                up.skipped+=1
            up.status="".join(sl)
            up.save()   
            return render(request,'mainapp/questions.html',{'q':q,'ansform':ansform,})
        else:
            ansform=AnswerForm(request.POST)
            return render(request,'mainapp/questions.html',{'q':q,'ansform':ansform,})


def question_list(request, build_id):
    up = UserProfile.objects.get(user=request.user)
    sl=list(up.status)
    building=Building.objects.get(pk=build_id)
    questions = Question.objects.filter(building_context=building)
    return render(request,'mainapp/question_list.html',{'questions':questions,'sl':sl,'building':building})
