from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('over', views.over, name='over'),
    path('', views.index, name='index'),
]
