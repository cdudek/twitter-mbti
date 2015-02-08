__author__ = 'cata'
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
import genrate_histogram as gh

DIR = os.path.dirname(os.path.realpath(__file__))
print DIR

def home(request):
    return render(request, DIR + '/templates/form.html')

handle = ""
def handleProcess(request):
    print request.POST
    handle = request.POST[u'handle']
    # do magic and generate image(handle)
    # generate foopage
    return HttpResponseRedirect("/results")

def results(request):
    #names = gh.getPLotFromTypeCounts(handle)
    names = ["samuel\nAnna", "alexander", "fsdfsd", "dhtyjt", "tjyujyu", "yukyukyu", "tyukr", "ertyeryt", "etyeryre", "ertyry", "fjtj", "rtyutyu", "sfgseg", "segseg", "sgsergs", "dfgserg"]
    t = loader.get_template(DIR + '/templates/foopage.html')
    c = Context({ "names" : names })
    print "rendering template"
    return HttpResponse(t.render(c))
