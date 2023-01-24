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


def addSource(request):
    if (request.method == "POST"):
        try:
            match = re.match(r"^(?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})){3}$",
                             request.POST['ip'])
            if match is None:
                return render(request, 'app/addSource.html', {
                    'error_message': 'IP адрес не соответствует шаблону!',
                })

            newSource = Source.objects.create(ip_adress=request.POST['ip'],
                               video_feed_name=request.POST['feed'],
                               name=request.POST['descr'])
            newSource.save()
        except (KeyError):
            return render(request, 'app/addSource.html', {
                'error_message': 'Не все данные были заполнены!',
            })
        else:
            return HttpResponseRedirect(reverse('app:index'))
    if (request.method == "GET"):
        return render(request, 'app/addSource.html')


def removeSource(request, **kwargs):
    instance = Source.objects.get(id=kwargs['id'])
    instance.delete()
    return HttpResponseRedirect(reverse('app:index'))

def selectSource(request, **kwargs):
    instance = Source.objects.get(id=kwargs['id'])
    return HttpResponseRedirect(reverse('app:index'))


def addTarget(request):
    return HttpResponse("Adding new target")


def gen(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

def videoFeed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
