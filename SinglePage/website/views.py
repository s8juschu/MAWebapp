from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
import json
from .models import Study, TaskSet, Task, Answer, Questionnaire, Question, Choice
from django.contrib.sessions.models import Session

study_id = 1  # TestStudy
overall_count = 15 # Nr. of cards

@property
def get_question(self):
    return Question.objects.filter(questionnaire=self.name)


@ensure_csrf_cookie
def index(request):
    tasks = Task.objects.all()
    # tasks = Task.objects.objects.filter(swimmer=swimmer)
    task_count = tasks.count()
    print("# tasks:" + str(task_count))

    # question_count = 0
    # questionnaires = Questionnaire.objects.filter(study=study_id)
    # for qs in questionnaires:
    #     questions = Question.objects.filter(questionnaire=qs)
    #     for q in questions:
    #         question_count += 1
    # print("# questions:" + str(question_count))

    # questions = Question.objects.all()
    # question_count = questions.count()

    page_nr = request.session.get('page_nr', '0')
    progress = request.session.get('progress', '0')
    # TODO delete whole IF
    print(page_nr)
    print(task_count)
    if page_nr == overall_count or page_nr > overall_count:
        request.session['page_nr'] = 0
        page_nr = request.session['page_nr']
        request.session['progress'] = 0
        progress = request.session['progress']
    return render(request, 'index.html',
                  context={"tasks": tasks, "task_count": task_count, "page_nr": page_nr, "overall_count": overall_count, "progress": progress})


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
        question_nr_exist = Answer.objects.filter(question_nr=current_page, session=session).exists()
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


def evaluation(request):
    if request.user.is_superuser:
        array = []
        sessions = Session.objects.all()
        print(sessions[1])
        for r in request.session.items():
            print(r)
        # for session in sessions:
        #     if Answer.objects.filter(session=session.session_key).exists():
        #         answer = Answer.objects.get(session=id)
        #         array.append(answer)
        #         return render(request, 'eval.html', context={"array": array})
        #     else:
        #         return HttpResponseRedirect(reverse('index'))
        # return render(request, 'eval.html', context={"sessions": sessions})
    else:
        return HttpResponseRedirect(reverse('index'))
