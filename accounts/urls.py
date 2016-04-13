from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^profile/(?P<username>\w+)/$', views.profile_page, name='profile_page'),
    url(r'^signup/$', views.new_user_page, name='new_user_page'),
    url(r'^thanks/(?P<username>\w+)/$', views.thank_you, name='thank_you'),
    url('^', include('django.contrib.auth.urls')),
    url('^home/$', views.home, name='home'),
    url('^friends/$', views.friends_page, name='friends_page'),
    url('^friend_someone', views.friend_someone, name='friend_someone'),
]