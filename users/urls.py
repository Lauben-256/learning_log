""" Defines URL patterns for users """
from django.conf.urls import url, include
from django.contrib.auth  import login
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
app_name = 'users'
urlpatterns = [
    # Login page
    #url('login/', login, {'template_name': 'users/login.html'}, name = 'login'),
    url('login/', LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
]