__author__ = 'cata'
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

DIR = os.path.dirname(os.path.realpath(__file__))
print DIR

def home(request):
    return render(request, DIR + '/templates/form.html')


def handleProcess(request):
    print request.POST
    handle = request.POST[u'handle']
    # do magic and generate image(handle)
    # generate foopage
    return HttpResponseRedirect("/results")

def results(request):
    print os.environ['HOME']
    mydict = {0: "sam", 1: "alex"}
    return render(request, DIR + '/templates/foopage.html')
