""" Defines URL patterns for learning_logs. """

from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('', views.index, name = 'index'),
    path('topics/', views.topics, name = 'topics'),
    path('topics/<int:id>/', views.topic, name = 'topic')
]