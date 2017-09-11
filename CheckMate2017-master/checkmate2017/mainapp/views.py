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
    if up is None or 1:
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
                'status':1,
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
            return HttpResponse('The game is not started yet! hold your horses boii :p')

def game(request):
    if not (request.user).is_authenticated() or (request.user.username) == "admin":
        return redirect('mainapp:login')
    else:
        up = UserProfile.objects.get(user=request.user)
        switch=GameSwitch.objects.get(name='main')
        
        if up.logstat==1 and request.method=='GET':
            return redirect('mainapp:congrats')
        
        else:
            buildings = Building.objects.all()
            d={}
            if 'bquery' in request.POST:
                if switch.end_game==1:
                    up.logstat=1
                    resp={
                    'status':'error',
                    'msg':'Time up'
                    }
                    return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
                bquery = request.POST['bquery']
                bl = Building.objects.get(building_name=bquery)
                qs = Question.objects.filter(building_context=bl)
                for i in qs:
                    d[i.pk-1]=json.loads(serializers.serialize('json', [i,]))
                return HttpResponse(json.dumps(d), content_type = "application/json")
            return render(request, 'mainapp/game.html',{'up':up,'buildings':buildings})

def question(request):
        up = UserProfile.objects.get(user=request.user)
        sl= list(up.status)
        at= list(up.attempts)
        bs= list(up.bstat)
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
                    if sl[index]=="1":
                        return HttpResponse("Already attempted this question correctly!" ,content_type = "application/json")
                    elif int(at[index])>=3 and sl[index]=="0":
                        return HttpResponse("Maximum attempts reached" ,content_type = "application/json")
                    else:
                        if at[index]=="2":
                            bs[index]="2"
                            up.bstat="".join(bs)
                        at[index]=str(int(at[index])+1)
                        if (q.answer).lower().strip() == (ans.lower()).strip():
                            sl[index]="1"
                            bs[index]="1"
                            up.status="".join(sl)
                            up.attempts="".join(at)
                            up.bstat="".join(bs)
                            up.score+=100
                            up.save()
                            resp={
                                'status':1,
                                'msg':'correct',
                                'attempts':at[index]
                            }
                        else :
                            up.status="".join(sl)
                            up.attempts="".join(at)
                            up.wrong_responses+=1
                            up.score-=25
                            up.save()
                            resp={
                                'status':2,
                                'msg':'incorrect',
                                'attempts':at[index]
                            }
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
        return HttpResponse("You chose to end the game! you cannot log back in anymore!",content_type = "application/json", status=500)
    return render(request,'mainapp/congrats.html')

def logout(request):
    django_logout(request)
    return render(request, 'mainapp/index.html')

def query(request):
    if request.user.is_authenticated():
        up=UserProfile.objects.get(user=request.user)
        bs= list(up.bstat)
        k=0
        phoda=[]
        lite=[]
        for i in bs:
            k+=1
            if i == '1':
                phoda.append(Building.objects.get(pk=k).building_name)
            if i == '2':
                lite.append(Building.objects.get(pk=k).building_name)
        if request.method=='POST' and 'player' in request.POST:
            sprite=request.POST['player']
            if sprite in ['boy','girl']:
                up.sprite=sprite
                up.save()
        resp={'player':up.sprite,'phoda':phoda,'lite':lite,}
        return HttpResponse(json.dumps(resp), content_type = "application/json")

    else:
        return HttpResponse("user not authenticated", content_type = "application/json")
