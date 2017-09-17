from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, Http404 ,HttpResponseForbidden
from .models import UserProfile, GameSwitch, Building, Question, Answer
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
from .leaderboard import pingservers
import urllib, requests, sys
from django.views.decorators.csrf import csrf_exempt

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
        print("reached0")
        form = TeamForm(request.POST)
        if request.method == 'POST' :
            if form.is_valid():
                print (form)
                print("reached1")
                data = form.cleaned_data
                u = User()
                u.username = data['teamname1']
                u.set_password(data['password1'])
                try:
                    u.save()
                except IntegrityError:
                    print("reached2")
                    resp={
                    'status': 'error',
                    'msg': 'Team name already registered or other conflicting entries'
                    }
                    return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
                up = UserProfile()
                up.user = u
                up.teamname = data['teamname1']
                up.idno1=data['idno1']
                up.idno2=data['idno2']
                up.ip_address = get_ip(request)
                up.save()
                #return redirect('mainapp:login')
                r={
                "status":"redirect",
                "url":"login"
                }
                print("reachedXXXX")
                return HttpResponse(json.dumps(r),content_type="application/json")
            else:
                error=json.loads(json.dumps(form.errors))
                error1=[]
                for e in error:
                    d=e
                    print("d",d)
                    if(d in ["password1","teamname1"]):
                        d=d[:-1]
                    error1.append(d)
                    error1.append('-')
                    error1.append((error[e])[0])
                    error1.append('<br/>')
                print(error1)
                resp={
                'status':'error',
                'msg':' '.join(error1)
                }
                print("reachedbbbbb")
                return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
        else:
            form=TeamForm(request.POST)
            r={
            "status":"redirect",
            "url":"login"
            }
            print("reached3")
            return HttpResponse(json.dumps(r),content_type="application/json",status=301)
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
            print("reachedl0")
            tform=TeamForm(request.POST)
            lform = LoginForm(request.POST)
            if request.method == 'POST':
                print("reachedl1")
                if lform.is_valid():
                    print("reachedl2")
                    data=lform.cleaned_data
                    teamname = data['teamname']
                    password = data['password']
                    user = authenticate(username = teamname, password=password)
                    if user is not None:
                        print("reachedl3")
                        auth.login(request, user)
                        return redirect(reverse('mainapp:game'))
                    else:
                        print("reachedl4")
                        resp={
                        'status':'error',
                        'msg':'Register before you try to Login!'
                        }
                        return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
                else:
                    error=json.loads(json.dumps(lform.errors))
                    error1=[]
                    for e in error:
                        d=e
                        print("d",d)
                        if(d in ["password1","teamname1"]):
                            d=d[:-1]
                        error1.append(d)
                        error1.append('-')
                        error1.append((error[e])[0])
                        error1.append('<br/>')
                    print(error1)
                    resp={
                    'status':'error',
                    'msg':' '.join(error1)
                    }
                    print("reachedbbbbb")
                    return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
            else:
                lform=LoginForm(request.POST)
                return render(request, 'mainapp/login.html',{'lform':lform,'tform':tform})
            return render(request, 'mainapp/login.html',{'lform':lform,'tform':tform})
        else:
            resp={
            'status':'error',
            'msg':'The game has not started yet',
            }
            return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)

def phode_lite(request):
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
        return [phoda, lite]


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
            [phoda, lite] = phode_lite(request)
            return render(request, 'mainapp/game.html',{'up':up,'buildings':buildings,"phoda": phoda, "lite": lite})

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
                a= Answer.objects.get(context=(Building.objects.get(building_name=q.building_context)))
                data=ansform.cleaned_data
                ans= data['answer']
                qs=Question.objects.all()
                resp={}

                if ans is not None:
                    if sl[index]=="1":
                        resp={
                        'status':'error',
                        'msg':"Already attempted this question correctly!"
                        }
                        return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
                    elif int(at[index])>=3 and sl[index]=="0":
                        resp={
                        'status':'error',
                        'msg':"Maximum attempts reached"
                        }
                        return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
                    else:
                        if at[index]=="2":
                            bs[index]="2"
                            up.bstat="".join(bs)
                        at[index]=str(int(at[index])+1)
                        if (a.answer).lower().strip() == (ans.lower()).strip():
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
                        [phoda, lite] = phode_lite(request)
                        resp['phoda'] = phoda
                        resp['lite'] = lite
                    up.status="".join(sl)
                    up.save()
                    return HttpResponse(json.dumps(resp), content_type = "application/json")


def congrats(request):
    if request.user.is_authenticated():
        up = UserProfile.objects.get(user=request.user)
        up.logstat=1
        up.save()
        a = up.score
    else:
        resp={
        'status':'error',
        'msg':'You chose to end the game! you cannot log back in anymore!'
        }
        return HttpResponse(json.dumps(resp), content_type = "application/json",status=500)
    return render(request,'mainapp/congrats.html', {'a':a})

def logout(request):
    django_logout(request)
    return render(request, 'mainapp/index.html')

def query(request):
    if request.user.is_authenticated():
        up=UserProfile.objects.get(user=request.user)

        if request.method=='POST' and 'player' in request.POST:
            sprite=request.POST['player']
            if sprite in ['boy','girl']:
                up.sprite=sprite
                up.save()
        resp={'player':up.sprite}
        return HttpResponse(json.dumps(resp), content_type = "application/json")

    else:
        return HttpResponse("user not authenticated", content_type = "application/json")

@csrf_exempt
def pingme(request):
        x=20
        up = UserProfile.objects.order_by('score')[:]
        n=len(up)
        up=up[n-x:]
        k=0
        d=[]
        x=""
        for i in up:
            if(i.score>0):
                d.append({
                'Teamname':i.teamname,
                'Score':i.score
                })
        d.reverse()
        return HttpResponse(json.dumps(d), content_type = "application/json")

@csrf_exempt
def pingservers(request):
    iplist=['127.0.0.1','127.0.0.1']
    all_list=[]
    i=0
    for ip in iplist:
        urlx='http://'+ip+':8000/pingme'
        client=requests.session()
        client.get(urlx)

        r = client.post(urlx, headers=dict(Referer=urlx))
        a=r.json()
        all_list.extend(a)
    sorted_all_list = sorted(all_list, key=lambda k: -k['Score'])

    return HttpResponse((json.dumps(sorted_all_list)), content_type = "application/json")

def leaderboard(request):
    if request.user.is_authenticated():
        return render(request,"mainapp/leaderboard.html")
    else:
        return HttpResponseForbidden()
