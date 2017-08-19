from django.contrib.auth.models import User
from django import forms
from .models import *

class TeamForm(forms.Form):
	teamname = forms.CharField(max_length=50,label='Team Name (Username):')
	password = forms.CharField(widget=forms.PasswordInput(),max_length=50)
	name1 = forms.CharField(max_length=50,label='Name of 1st Participant :')
	name2 = forms.CharField(max_length=50,required=False,label='Name of 2nd Participant(Optional) :')
	phone1 = forms.IntegerField(widget=forms.TextInput(),min_value=6000000000,label='Phone of 1st Participant :')
	phone2 = forms.IntegerField(widget=forms.TextInput(),required=False,min_value=6000000000,label='Phone of 2nd Participant(Optional) :')
	email1 = forms.EmailField(label='Email of 1st Participant :')
	email2 = forms.EmailField(required=False,label='Email of 2nd Participant(Optional) :')
	idno1 = forms.CharField(max_length=20)
	idno2 = forms.CharField(required=False,max_length=20)

class LoginForm(forms.Form):
        teamname=forms.CharField(max_length = 50)
        password=forms.CharField(widget=forms.PasswordInput())


class AnswerForm(forms.Form):
	answer=forms.CharField(max_length=100)
