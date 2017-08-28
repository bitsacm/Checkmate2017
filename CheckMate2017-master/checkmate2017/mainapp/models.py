from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import re
from django.core import validators


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) #extending user model
	teamname = models.CharField(max_length=200)
	#name1 = models.CharField(max_length=200)
	#name2 = models.CharField(max_length=200,blank=True)
	#phone1 = models.BigIntegerField(null=True,validators=[\
		#validators.RegexValidator(re.compile('^\d{10}$'),message='Enter the valid phone number.',code='Invalid!')])
	#phone2 = models.BigIntegerField(null=True,blank=False,validators=[\
		#validators.RegexValidator(re.compile('^\d{10}$'),message='Enter the valid phone number.',code='Invalid!')])

	#email1 = models.CharField(unique=True,null=False, max_length=34, \
			#help_text="The email id should be in this format: f201xxxxx@pilani.bits-pilani.ac.in",validators=[\
			#validators.RegexValidator(re.compile('^f201[0-9]{4,5}@pilani\.bits-pilani\.ac\.in'),\
				#message='Enter yor valid BITS-mail',code='invalid!')])
	#email2 = models.CharField(unique=True,null=True,blank=True, max_length=34, \
			#help_text="The email id should be in this format: f201xxxxx@pilani.bits-pilani.ac.in",validators=[\
			#validators.RegexValidator(re.compile('^f201[0-9]{4,5}@pilani\.bits-pilani\.ac\.in'),\
				#message='Enter yor valid BITS-mail',code='invalid!')])

	idno1 = models.CharField(max_length=20,validators=[\
		validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P$'),message='Enter your valid BITS-mail',code='invalid!')])
	idno2 = models.CharField(null=True,blank=False,max_length=20,validators=[\
		validators.RegexValidator(re.compile('^201[0-9]{1}[0-9A-Z]{4}[0-9]{4}P$'),message='Enter your valid BITS-mail',code='invalid!')])

	score = models.IntegerField(default=0)
	ip_address = models.CharField(null=True,max_length=20)
	status = models.CharField(max_length=40,default="0000000000000000000000000")
	build_solved= models.CharField(max_length=30,default="00000000000000000000000000")
	wrong_responses= models.IntegerField(default=0)
	#skipped= models.IntegerField(default=0)


	def __str__(self):
		return self.teamname

class Building(models.Model):
        building_name = models.CharField(max_length=100)
        q_total = models.IntegerField(default=1)

        def __str__(self):
                return self.building_name

class Question(models.Model):
        building_context = models.ForeignKey(Building,on_delete=models.CASCADE)
        points= models.IntegerField(null=False)
        question_text=RichTextField()
        answer = models.CharField(max_length=100)
        difficulty_level=models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')),default=1)

        def __str__(self):
                return "Question #"+str(self.pk)

class GameSwitch(models.Model):
		name=models.CharField(null=False,max_length=10)
		start_game = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default = 1)
		end_game = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default=0)#0 is switch status inactive, 1 is active

		def __str__(self):
				return self.name
