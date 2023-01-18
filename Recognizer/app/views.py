from django.shortcuts import render
from django.http import HttpResponse
from .models import SourceList

# Create your views here.
def index(request):
    sourceList = SourceList.objects.all()
    context = {'source_list': sourceList}
    return render(request, 'app/index.html', context)


def dayEncounter(request, day):
    response = "Encountered target in day %s"
    return HttpResponse(response % day)


def addSource(request):
    return HttpResponse("Adding new source")


def addTarget(request):
    return HttpResponse("Adding new target")
