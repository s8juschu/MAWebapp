from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
import json


cards = [
    {
        "id": 0,
        "title": "Participation information ",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
    {
        "id": 1,
        "title": "Question1",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
    {
        "id": 2,
        "title": "Question2",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
    {
        "id": 3,
        "title": "Question3",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
    {
        "id": 4,
        "title": "Question4",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
]

# def redirect(request):
#     page_nr = request.session.get('page_nr', 0)
#     request.session['page_nr'] = page_nr
#     print(request.session['page_nr'])
#     if request.session['page_nr'] == 0:
#         print("index")
#         request.session['page_nr'] = page_nr+1
#         return index(request)
#     if request.session['page_nr'] == 1:
#         request.session['page_nr'] = page_nr + 1
#         return page1(request)
#     if request.session['page_nr'] == 2:
#         return page2(request)
#     else:
#         return render(request, "index.html")
#     # del (request.session['page_nr'])


def index(request):
    # del (request.session['page_nr'])
    page_nr = request.session.get('page_nr', 0)
    request.session['page_nr'] = page_nr
    # if page_nr > 4: del (request.session['page_nr'])
    return render(request, 'index.html', context={"cards": cards})

#
# def page1(request):
#     page_nr = request.session['page_nr']
#     return render(request, 'page1.html', {"page_nr": page_nr})
#
#
# def page2(request):
#     page_nr = request.session['page_nr']
#     return render(request, 'page2.html', {"page_nr": page_nr})
