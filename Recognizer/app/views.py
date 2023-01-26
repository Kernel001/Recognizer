from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
from django.views import generic

from .camera import VideoCamera
from .models import Source

import re


class SourceDetailView(generic.DetailView):
    model = Source
    #template_name = 'app/sourceDetail.html'

class SourceListView(generic.ListView):
    model = Source
    #template_name = 'app/sourceDetail.html'
    #context_object_name = 'source_list'


# Create your views here.
def index(request):
    sourceList = Source.objects.all()
    context = {'source_list': sourceList}
    return render(request, 'app/index.html', context)

def dayEncounter(request, **kwargs):
    response = "Encountered target in day %s"
    return HttpResponse(response % kwargs['encDay'])

def removeSource(request, **kwargs):
    instance = Source.objects.get(id=kwargs['id'])
    instance.delete()
    return HttpResponseRedirect(reverse('app:index'))

def selectSource(request, **kwargs):
    instance = Source.objects.get(id=kwargs['id'])
    return HttpResponseRedirect(reverse('app:index'))

def sources(request, **kwargs):
    sourceList = Source.objects.all()
    context = {'source_list': sourceList}
    return render(request, 'app/sourceContent.html', context)

def addTarget(request):
    return HttpResponse("Adding new target")


def gen(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

def videoFeed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
