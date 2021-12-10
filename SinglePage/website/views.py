from django.shortcuts import render
from django.http import HttpResponse
import json


cards = [
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
    {
        "id": 5,
        "title": "Question5",
        "text": "INSERT TEXT",
        "image": "INSERT IMG",
    },
]


def index(request):
    card_count = 6
    page_nr = request.session.get('page_nr', '0')
    progress = request.session.get('progress', '0')
    print(progress)
    print(page_nr)
    if page_nr == 6:
        request.session['page_nr'] = 0
        page_nr = request.session['page_nr']
        request.session['progress'] = 0
        progress = request.session['progress']
    return render(request, 'index.html', context={"cards": cards, "page_nr": page_nr, "card_count": card_count, "progress": progress})


def saveSession(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    print("save" + str(parameterinfo["page"]))

    page = parameterinfo["page"]
    request.session['page_nr'] = page
    page_nr = request.session['page_nr']

    progress = parameterinfo["progress"]
    request.session['progress'] = progress
    progress = request.session['progress']
    print(progress)

    return HttpResponse(200)
