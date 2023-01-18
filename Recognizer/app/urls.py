from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('encounters/<int:encDay>/', views.dayEncounter, name='encounterDay'),
    path('addSource/', views.addSource, name='addSource'),
    path('addTarget/', views.addTarget, name='addTarget'),
]