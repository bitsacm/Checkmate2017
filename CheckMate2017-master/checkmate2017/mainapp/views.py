from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserProfile, GameSwitch, Building, Question
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login, logout as django_logout
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
    if not request.user.is_authenticated or request.user.username == "admin":
        return render(request, 'mainapp/index.html',)
    else:
        return redirect('mainapp:game')

def register(request):
    up = UserProfile.objects.filter(ip_address=get_ip)
    if up is None or 1:#this is for developement time being
        form = TeamForm(request.POST)
        if request.method == 'POST' and 'register-submit' in request.POST:
            if form.is_valid():
                data = form.cleaned_data
                u = User()
                u.username = data['teamname1']
                u.set_password(data['password1'])
                try:
                    u.save()
                except IntegrityError:
                    resp={
                    'status': 1,
                    'error': 'Team name already registered or other conflicting entries'
                    }
                    return HttpResponse(json.dumps(resp), content_type = "application/json")
                up = UserProfile()
                up.user = u
                up.teamname = data['teamname1']
                up.idno1=data['idno1']
                up.idno2=data['idno2']
                up.ip_address = get_ip(request)
                up.save()
                return redirect('mainapp:login')
            else:
                resp={
                'status':2,
                'error':'Failed! Invalid login attempt, make sure that you used your own correct BITS mail and id!'
                }
                return HttpResponse(json.dumps(resp), content_type = "application/json")
        else:
            form=TeamForm(request.POST)
            return render(request,'mainapp/login.html',{'form':form})
        return render(request,'mainapp/login.html',{'form':form})
    else:
        return HttpResponse('You have already registered once from this pc! Contact neartest ACM invigilator')
    

def instructions(request):
    return render(request, 'mainapp/instructions.html')

def login(request):
    if request.user.is_authenticated() and not request.user.username == "admin":
        return redirect('mainapp:game')
    else:
        g=GameSwitch.objects.get(name='main')
        if g.start_game:
            tform=TeamForm(request.POST)
            lform = LoginForm(request.POST)
            if request.method == 'POST' and 'login-submit' in request.POST:
                if lform.is_valid():
                    data=lform.cleaned_data
                    teamname = data['teamname']
                    password = data['password']
                    user = authenticate(username = teamname, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect(reverse('mainapp:game'))
                    else:
                        return HttpResponse("Do not forget to register before login :p !")
                else:
                    print ( lform.errors )
            else:
                lform=LoginForm(request.POST)
                return render(request, 'mainapp/login.html',{'lform':lform,'tform':tform})
            return render(request, 'mainapp/login.html',{'lform':lform,'tform':tform})
        else:
            return HttpResponse('The game is not started yet, or it has already ended')

def game(request):
    if not (request.user).is_authenticated() or (request.user.username) == "admin":
        return redirect('mainapp:login')
    else:
        up = UserProfile.objects.get(user=request.user)
        switch=GameSwitch.objects.get(name='main')
        if switch.end_game==1:
            up.logstat=1
            resp={
            'status':0,
            'error':'Time up!'
            }
            return HttpResponse(json.dumps(resp), content_type = "application/json")
        if up.logstat==1:
            return redirect('mainapp:congrats')
        else:
            buildings = Building.objects.all()
            d={}
            if 'bquery' in request.POST:
                bquery = request.POST['bquery']
                bl = Building.objects.get(building_name=bquery)
                qs = Question.objects.filter(building_context=bl)
                for i in qs:
                    d[i.pk-1]=json.loads(serializers.serialize('json', [i,]))
                return HttpResponse(json.dumps(d), content_type = "application/json")

            question = Question.objects.all()
            sl= list(up.status)
            bs= list(up.build_solved)
            up.score=0
            for q in question:
                ch = sl[q.pk-1]
                if ch=='2':
                    up.score+=100
            up.score-= (up.wrong_responses*25)
            up.build_solved="".join(bs)
            up.save()
            return render(request, 'mainapp/game.html',{'up':up,'bs':bs,'buildings':buildings})

def question(request):
        print(request)
        up = UserProfile.objects.get(user=request.user)
        sl= list(up.status)
        ansform=AnswerForm(request.POST)
        if request.method == 'POST' and 'pkvalue' in request.POST:
            if ansform.is_valid():

                ques_id=request.POST['pkvalue']
                index = int(ques_id)-1
                q = Question.objects.get(pk=ques_id)
                data=ansform.cleaned_data
                ans= data['answer']
                qs=Question.objects.all()
                resp={}

                if ans is not None:
                    print(q.answer,ans)
                    if sl[index]=="2":
                        return HttpResponse("Already attempted this question once!")
                    else:
                        if (q.answer).lower().strip() == (ans.lower()).strip():
                            sl[index]="2"
                            up.status="".join(sl)
                            up.save()
                            resp={
                                'status':1,
                            }
                            print("inside_correct",up.wrong_responses)

                        else :
                            #sl[index]="3"
                            up.status="".join(sl)
                            up.wrong_responses+=1
                            print(up.wrong_responses)
                            up.save()
                            resp={
                                'status':2,
                            }
                        up.score=0
                        for qx in qs:
                            ch = sl[int(qx.pk)-1]
                            if ch=='2':
                                up.score+=100
                        up.score-=(up.wrong_responses*25)
                        up.save()
                        skore=up.score
                        resp['score']=skore

                    up.status="".join(sl)
                    up.save() 
                    return HttpResponse(json.dumps(resp), content_type = "application/json")


def congrats(request):
    if request.user.is_authenticated():
        up = UserProfile.objects.get(user=request.user)
        up.logstat=1
        up.save()
    else:
        return HttpResponse("You chose to end the game! you cannot log back in anymore!")
    return render(request,'mainapp/congrats.html')

def logout(request):
    django_logout(request)
    return render(request, 'mainapp/index.html')