from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^instructions$', views.instructions, name='instructions'),
    url(r'^game$', views.game, name='game'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^question_list/(\d+)/question/(?P<ques_id>\d+)/$',views.question,name='question'),
    url(r'^question_list/(?P<build_id>\d+)/$',views.question_list,name='question_list'),
]
