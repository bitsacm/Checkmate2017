from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserProfile, GameSwitch
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .forms import TeamForm, LoginForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from .controls import get_client_ip


def test(request):
    return HttpResponse('Fack! it is working :D')
    
def index(request):
    u= User.objects.filter(pk=get_client_ip(request))
    if u is None or u is 'admin':    
        return render(request, 'mainapp/index.html',)
    else:
        return redirect('login')

def register(request):
    form = TeamForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            u = User()
            u.username = data['teamname']
            u.set_password(data['password'])
            try:
                u.save()
                u.pk = get_client_ip(request)
            except IntegrityError:
                return HttpResponse('Team name already registered')
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
            up.save()
            return redirect('login')
    return render(request,'mainapp/register.html',{'form':form})
    

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
                    return render(request,'mainapp/game.html')
            else:
                return HttpResponse('Invalid form')
        else:
            lform=LoginForm(request.POST)
            return render(request, 'mainapp/login.html',{'lform':lform,})
        return render(request, 'mainapp/login.html',{'lform':lform,})
    else:
        return HttpResponse('The game is not started yet, or it has already ended')