from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^instructions$', views.instructions, name='instructions'),
    url(r'^game$', views.game, name='game'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^congrats$', views.congrats, name = 'congrats'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^question$',views.question,name='question'),
    url(r'^question_list/(?P<build_id>\d+)/$',views.question_list,name='question_list'),
]
