from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
import json
from .models import Study, Questionnaire, Question, Answer
from django.contrib.sessions.models import Session

study_id = 1  # TestStudy


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

@ensure_csrf_cookie
def index(request):
    # Nr of Tasks
    card_count = 6
    page_nr = request.session.get('page_nr', '0')
    progress = request.session.get('progress', '0')
    # TODO delete whole IF
    if page_nr == card_count:
        request.session['page_nr'] = 0
        page_nr = request.session['page_nr']
        request.session['progress'] = 0
        progress = request.session['progress']
    return render(request, 'index.html',
                  context={"cards": cards, "page_nr": page_nr, "card_count": card_count, "progress": progress})

@ensure_csrf_cookie
def saveSession(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    # Save which page to display next
    print("Next page:" + str(parameterinfo["page"]))
    next_page = parameterinfo["page"]
    current_page = (next_page - 1)
    request.session['page_nr'] = next_page

    # Save progressbar status
    progress = parameterinfo["progress"]
    request.session['progress'] = progress

    if 'answer' in parameterinfo:
        study = Study.objects.get(pk=study_id)
        session = Session.objects.get(session_key=request.session.session_key)
        print(session)
        question_nr_exist = Answer.objects.filter(question_nr=current_page).exists()
        if not question_nr_exist:
            answer = parameterinfo["answer"]
            answer_model = Answer()
            answer_model.answer = answer
            answer_model.study = study
            answer_model.session = session
            answer_model.question_nr = current_page
            answer_model.save()

            print(Answer.objects.all())
            print(Session.objects.all())
        else:
            print("Already done that task. Not saved.")
    return HttpResponse(200)
