from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
import json


def nextpage(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    print(parameterinfo)

    page = parameterinfo["page"]
    request.session['page_nr'] = page
    return HttpResponseRedirect(reverse('page'+page))
