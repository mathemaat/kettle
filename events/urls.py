from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('melding-maken', views.melding_maken, name='melding-maken'),
    path('over', views.over, name='over'),
    path('', views.index, name='index'),
]
