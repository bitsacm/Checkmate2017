from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) #extending user model
	teamname = models.CharField(max_length=200)
	name1 = models.CharField(max_length=200)
	name2 = models.CharField(max_length=200,blank=True)
	phone1 = models.BigIntegerField(null=True)
	phone2 = models.BigIntegerField(blank=True,null=True)
	email1 = models.EmailField()
	email2 = models.EmailField(blank=True,null=True)
	idno1 = models.CharField(max_length=20)
	idno2 = models.CharField(max_length=20,blank=True)


	def __str__(self):
		return self.teamname

class Building(models.Model):
        building_name = models.CharField(max_length=100)
        difficulty_level = models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')),default=1)

        def __str__(self):
                return self.building_name

class Question(models.Model):
        building_context = models.ForeignKey(Building)
        points= models.IntegerField(null=False)
        question_text=RichTextField()
        answer= models.CharField(max_length=100)
        status = models.IntegerField(null=False, choices=((0,'0'),(1,'1'),(2,'2')),default=1)#0 is unattempted, 1 is skipped, 2 is solved!

        def __str__(self):
                return "Question #"+str(self.pk)

class GameSwitch(models.Model):
		name=models.CharField(null=False,max_length=10)
		start_game = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default = 1)
		end_game = models.IntegerField(null=False, choices=((0,'0'),(1,'1')),default=0)#0 is switch status inactive, 1 is active

		def __str__(self):
				return self.name


