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
    url(r'^query$',views.query,name='query'),
    url(r'^pingme$',views.pingme,name='pingme'),
    url(r'^pingservers$',views.pingservers,name='pingservers'),
    url(r'^leaderboard$',views.leaderboard,name='leaderboard'),
]
