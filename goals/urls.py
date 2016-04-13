from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<goal_id>\d+)/$', views.goal_detail_page, name='goal_detail_page'),
    url(r'^(?P<goal_id>\d+)/step/(?P<step_id>\d+)/$', views.step_detail_page, name='step_detail_page'),
    url(r'^(?P<username>\w+)/set_goal/$', views.goal_setting_page, name='goal_setting_page'),
    url(r'^(?P<goal_id>\d+)/create_steps/$', views.step_creation_page, name='step_creation_page'),
    url(r'^(?P<goal_id>\d+)/edit/$', views.edit_goal, name='edit_goal'),
    url(r'^step_completion/$', views.step_completion, name='step_completion'),
]