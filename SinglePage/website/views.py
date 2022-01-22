from distutils.util import strtobool
import json
from collections import defaultdict
from random import shuffle
import random

from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.template.defaultfilters import register
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Study, TaskSet, Task, Submission, AnswerChoice, Question, TaskSubmission

study_id = 1  # TestStudy
overall_count = 12  # Nr. of cards


# Split List in two
def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


# Distribute 2 of each task randomly into one task set
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


# Load list from session var
def load_lists(request, p1, p2, m1, m2):
    list_p1 = []
    list_p2 = []
    list_m1 = []
    list_m2 = []
    array = defaultdict(list)

    request.session['p1'] = p1
    request.session['p2'] = p2
    request.session['m1'] = m1
    request.session['m2'] = m2

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

    return list_p1, list_p2, list_m1, list_m2


# Returns the possible Answer choices for a given task
def get_choices(list_object):
    array = defaultdict(list)
    for l in list_object:
        if AnswerChoice.objects.filter(task=l).exists():
            choice = AnswerChoice.objects.filter(task=l)
            for c in choice:
                array[l.pk].append(c.text)

    arraydict = dict(array)  # transform defaultdict to dict
    # print(arraydict)

    return arraydict


# Returns the given key from a dictionary
@register.filter(name='dict_key')
def dict_key(d, k):
    return d.get(k)


# Assign randomly to one of 3 groups
# 0: control group
# 1: pos framing
# 2: neg framing
def get_condition():
    rnd = random.randint(0, 2)
    return rnd


def save_initialization(request, list_p1, list_p2, list_m1, list_m2):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    session = Session.objects.get(session_key=request.session.session_key)
    print(session)
    if not Submission.objects.filter(session=session).exists():
        submission = Submission()
        submission.study = Study.objects.get(pk=study_id)
        submission.session = session
        submission.list_p1 = list_p1
        submission.list_p2 = list_p2
        submission.list_m1 = list_m1
        submission.list_m2 = list_m2
        submission.save()


@ensure_csrf_cookie
def index(request):
    list_p1 = []
    list_p2 = []
    list_m1 = []
    list_m2 = []

    # Initialize to either old value or 0 if not exists
    page_nr = request.session.get('page_nr', '0')
    progress = request.session.get('progress', '0')
    p1 = request.session.get('p1', '0')
    p2 = request.session.get('p2', '0')
    m1 = request.session.get('m1', '0')
    m2 = request.session.get('m2', '0')

    # Assign randomly to condition
    r = get_condition()
    rnd = request.session.get('rand', r)
    print("rand:" + str(rnd))

    # Load answers from questionnaire
    imi = Question.objects.filter(questionnaire__name="Intrinsic Motivation Inventory")
    # print(imi)

    if 'init' not in request.session:
        request.session['init'] = 'true'

        p1, p2, m1, m2 = randomize_tasks()
        list_p1, list_p2, list_m1, list_m2 = load_lists(request, p1, p2, m1, m2)

        array_p1 = get_choices(list_p1)
        array_p2 = get_choices(list_p2)
        array_m1 = get_choices(list_m1)
        array_m2 = get_choices(list_m2)

    elif request.session.get('init') == 'true':
        # name = request.session.session_key
        list_p1, list_p2, list_m1, list_m2 = load_lists(request, p1, p2, m1, m2)

        array_p1 = get_choices(list_p1)
        array_p2 = get_choices(list_p2)
        array_m1 = get_choices(list_m1)
        array_m2 = get_choices(list_m2)

        # print(name, list_p1, list_p2, list_m1, list_m2)

    else:
        print("error")

    save_initialization(request, list_p1, list_p2, list_m1, list_m2)

    # TODO delete whole IF
    print(page_nr)
    if (int(page_nr) == overall_count) or (int(page_nr) > overall_count):
        request.session['page_nr'] = 0
        page_nr = request.session['page_nr']
        request.session['progress'] = 0
        progress = request.session['progress']
        del (request.session['init'])

    return render(request, 'index.html',
                  context={"m1": list_m1, "m2": list_m2, "p1": list_p1, "p2": list_p2,
                           "array_m1": array_m1, "array_m2": array_m2, "array_p1": array_p1, "array_p2": array_p2,
                           "page_nr": page_nr, "overall_count": overall_count, "progress": progress,
                           "framing": rnd, "imi": imi})


# Save next page & progressbar to show on press continue in frontend
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

    return HttpResponse(200)


# Save personal info from frontend in DB
@ensure_csrf_cookie
def saveData(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    if submission_exist:
        # Save if participant agreed data terms
        if parameterinfo["type"] == 'agree':
            # Only save if entry not yet saved
            if Submission.objects.filter(session=session, terms_agree="False").exists():
                agree = parameterinfo["agree"]
                submission = Submission.objects.get(session=session)
                submission.terms_agree = bool(strtobool(agree))
                print(agree)
                submission.save()
            else:
                print("Already saved terms_agree info. No changes made to DB.")

        # Save if participants personal info
        if parameterinfo["type"] == 'personal':
            if Submission.objects.get(session=session).age == "" and \
                    Submission.objects.get(session=session).gender == "":
                age = parameterinfo["age"]
                nationality = parameterinfo["nationality"]
                gender = parameterinfo["gender"]
                submission = Submission.objects.get(session=session)
                submission.age = age
                submission.nationality = nationality
                submission.gender = gender
                print(age + nationality + gender)
                submission.save()
            else:
                print("Already saved personal info. No changes made to DB.")

        # Save if participant finished study
        if parameterinfo["type"] == 'finish':
            # Only save if entry not yet saved
            if Submission.objects.filter(session=session, finished="False").exists():
                finish = parameterinfo["finish"]
                submission = Submission.objects.get(session=session)
                submission.finished = bool(strtobool(finish))
                print(finish)
                submission.save()
            else:
                print("Already saved finished info. No changes made to DB.")

    else:
        print("ERROR: Submission does not exist.")

    return HttpResponse(200)


# Save tasks answers from frontend in DB
@ensure_csrf_cookie
def saveTask(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    print(parameterinfo)

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()
    par_type = parameterinfo["type"]

    if submission_exist:
        listitem = parameterinfo["listarray"]
        for item in listitem:
            task_item = item["item"]
            if not TaskSubmission.objects.filter(session=session, type=par_type, item=task_item).exists():
                task_sub = TaskSubmission()
                task_sub.submission = Submission.objects.get(session=session)
                task_sub.session = session
                task_sub.type = par_type

                task_sub.item = task_item
                task_sub.task_id = item["task_id"]
                task_sub.answer = item["answer"]

                task_sub.save()

            else:
                print("Already saved task info of type:" + str(par_type) + ", item:" + str(task_item) +
                      ". No changes made to DB.")

    return HttpResponse(200)


# Save answers of IMI from frontend in DB
@ensure_csrf_cookie
def saveIMI(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    return HttpResponse(200)


# Save answers of PXI from frontend in DB
# @ensure_csrf_cookie
# def savePXI(request):
#     getparameterinfo = request.body.decode('utf-8')
#     parameterinfo = json.loads(getparameterinfo)


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
