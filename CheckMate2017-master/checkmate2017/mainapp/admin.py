from django.contrib import admin
from .models import Answer,UserProfile, Question, Building, GameSwitch
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Building)
admin.site.register(GameSwitch)
admin.site.register(Answer)

