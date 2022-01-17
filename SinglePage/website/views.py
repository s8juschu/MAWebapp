from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from random import shuffle
import json
from .models import Study, TaskSet, Task, Answer, Questionnaire, Question
from django.contrib.sessions.models import Session

study_id = 1  # TestStudy
overall_count = 12  # Nr. of cards


def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]


def randomize_tasks():
    pre_tasks = []  # First set of tasks
    main_tasks = []  # Second set of tasks
    tasksets = TaskSet.objects.all()
    for taskset in tasksets:
        tasks = Task.objects.filter(task_set=taskset).order_by('?')
        iterate_count = 0
        for task in tasks:
            if iterate_count < 2:
                iterate_count += 1
                pre_tasks.append(task.id)
            elif iterate_count >= 2:
                main_tasks.append(task.id)
                iterate_count += 1

    # Shuffle sets to randomize order
    shuffle(pre_tasks)
    pre1, pre2 = split_list(pre_tasks)
    shuffle(main_tasks)
    main1, main2 = split_list(main_tasks)

    return pre1, pre2, main1, main2


@ensure_csrf_cookie
def index(request):
    list_p1 = []
    list_p2 = []
    list_m1 = []
    list_m2 = []

    # Initialize to either old value or 0
    page_nr = request.session.get('page_nr', 'false')
    progress = request.session.get('progress', '0')

    p1 = request.session.get('p1', '0')
    p2 = request.session.get('p2', '0')
    m1 = request.session.get('m1', '0')
    m2 = request.session.get('m2', '0')

    # Distribute 2 of each task randomly into one task set
    if 'init' not in request.session:
        request.session['init'] = 'true'

        p1, p2, m1, m2 = randomize_tasks()

        request.session['p1'] = p1
        request.session['p2'] = p2
        request.session['m1'] = m1
        request.session['m2'] = m2

        p1 = request.session['p1']
        p2 = request.session['p2']
        m1 = request.session['m1']
        m2 = request.session['m2']

        for p in p1:
            task = Task.objects.get(pk=p)
            list_p1.append(task)
        for p in p2:
            task = Task.objects.get(pk=p)
            list_p2.append(task)
        for p in m1:
            task = Task.objects.get(pk=p)
            list_m1.append(task)
        for p in m2:
            task = Task.objects.get(pk=p)
            list_m2.append(task)

    elif request.session.get('init') == 'true':
        name = request.session.session_key
        p1 = request.session['p1']
        p2 = request.session['p2']
        m1 = request.session['m1']
        m2 = request.session['m2']

        for p in p1:
            task = Task.objects.get(pk=p)
            list_p1.append(task)
        for p in p2:
            task = Task.objects.get(pk=p)
            list_p2.append(task)
        for p in m1:
            task = Task.objects.get(pk=p)
            list_m1.append(task)
        for p in m2:
            task = Task.objects.get(pk=p)
            list_m2.append(task)
    else:
        print("error")

    # TODO delete whole IF
    print(page_nr)
    if (int(page_nr) == overall_count) or (int(page_nr) > overall_count):
        request.session['page_nr'] = 0
        page_nr = request.session['page_nr']
        request.session['progress'] = 0
        progress = request.session['progress']
        del(request.session['init'])

    return render(request, 'index.html',
                  context={"m1": list_m1, "m2": list_m2, "p1": list_p1, "p2": list_p2, "page_nr": page_nr,
                           "overall_count": overall_count, "progress": progress})


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


@ensure_csrf_cookie
def saveIMI(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)


@ensure_csrf_cookie
def savePXI(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)


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
