from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('removeSource/<int:id>/', views.removeSource, name='removeSource'),
    path('sources/', views.sources, name='sources'),

    path('video_feed', views.videoFeed, name="videoFeed"),

    path('addTarget/', views.addTarget, name='addTarget'),

    path('encounters/<int:encDay>/', views.dayEncounter, name='encounterDay'),
]