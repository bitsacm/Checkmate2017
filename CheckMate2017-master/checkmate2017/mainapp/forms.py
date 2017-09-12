from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
import re
from django.core import validators

class TeamForm(forms.Form):
	teamname1 = forms.CharField(max_length=50)
	password1 = forms.CharField(widget=forms.PasswordInput(),max_length=50)
	idno1 = forms.CharField(max_length=20,validators=[\
		validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P'),message='BITS ID of teammate 1 is empty or invalid',code='invalid!')])
	idno2 = forms.CharField(required=False,max_length=20,validators=[\
		validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P'),message='BITS ID of teammate 2 is empty or invalid',code='invalid!')])


class LoginForm(forms.Form):
        teamname=forms.CharField(max_length = 50)
        password=forms.CharField(widget=forms.PasswordInput())


class AnswerForm(forms.Form):
	answer=forms.CharField(required=True,max_length=100)
	pkvalue=forms.CharField(max_length=100)