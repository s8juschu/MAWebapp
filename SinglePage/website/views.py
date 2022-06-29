from distutils.util import strtobool
import json
from collections import defaultdict
from random import shuffle
import random
import csv

from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.template.defaultfilters import register
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
import time

from .models import Study, TaskSet, Task, Submission, AnswerChoice, Question, TaskSubmission, QuestionnaireSubmission, \
    TaskScore, TimeSpend, ExtraTask, ExtraAnswerChoice, ExtraTaskSubmission

study_id = 2  # Study
overall_count = 16  # Nr. of cards

# Load answers from questionnaire
imi = Question.objects.filter(questionnaire__name="Intrinsic Motivation Inventory")
panas = Question.objects.filter(questionnaire__name="PANAS")


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

    return arraydict


# Returns extra tasks and their possible Answer choices
def get_extraTasks():
    extratasks = ExtraTask.objects.all()
    array = defaultdict(list)
    for e in extratasks:
        if ExtraAnswerChoice.objects.filter(task=e).exists():
            choice = ExtraAnswerChoice.objects.filter(task=e)
            for c in choice:
                array[e.pk].append(c.text)

    arraydict = dict(array)  # transform defaultdict to dict

    return extratasks, arraydict


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
    if not Submission.objects.filter(session=session).exists():
        submission = Submission()
        submission.study = Study.objects.get(pk=study_id)
        submission.session = session
        submission.list_p1 = list_p1
        submission.list_p2 = list_p2
        submission.list_m1 = list_m1
        submission.list_m2 = list_m2
        submission.save()


@never_cache
@ensure_csrf_cookie
def index(request):
    list_p1 = []
    list_p2 = []
    list_m1 = []
    list_m2 = []

    # Initialize to either old value or 0 if not exists
    page_nr = request.session.get('page_nr', '0')
    request.session['page_nr'] = page_nr
    progress = request.session.get('progress', '0')
    request.session['progress'] = progress
    p1 = request.session.get('p1', '0')
    p2 = request.session.get('p2', '0')
    m1 = request.session.get('m1', '0')
    m2 = request.session.get('m2', '0')

    # Assign randomly to framing condition
    if 'rand' not in request.session:
        request.session['rand'] = get_condition()
    rnd = request.session.get('rand')

    if 'init' not in request.session:
        request.session['init'] = 'true'

        p1, p2, m1, m2 = randomize_tasks()
        list_p1, list_p2, list_m1, list_m2 = load_lists(request, p1, p2, m1, m2)

        array_p1 = get_choices(list_p1)
        array_p2 = get_choices(list_p2)
        array_m1 = get_choices(list_m1)
        array_m2 = get_choices(list_m2)

    elif request.session.get('init') == 'true':
        list_p1, list_p2, list_m1, list_m2 = load_lists(request, p1, p2, m1, m2)

        array_p1 = get_choices(list_p1)
        array_p2 = get_choices(list_p2)
        array_m1 = get_choices(list_m1)
        array_m2 = get_choices(list_m2)

    else:
        print("error")

    save_initialization(request, list_p1, list_p2, list_m1, list_m2)

    print(request.session.session_key)
    # print(page_nr)

    extratasks, extrachoices = get_extraTasks()

    # check if already finished study
    finish = finishedStudy(request)
    if page_nr == overall_count and finish is True:
        print("finish")
        return render(request, 'finish.html')

    return render(request, 'index.html',
                  context={"m1": list_m1, "m2": list_m2, "p1": list_p1, "p2": list_p2,
                           "array_m1": array_m1, "array_m2": array_m2, "array_p1": array_p1, "array_p2": array_p2,
                           "page_nr": page_nr, "overall_count": overall_count, "progress": progress,
                           "framing": rnd, "imi": imi, "panas": panas, "extratasks": extratasks,
                           "extrachoices": extrachoices})


# Save next page & progressbar to show on press continue in frontend
@ensure_csrf_cookie
def saveSession(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveSession" + " " + str(
            parameterinfo) + "\n")
        f.close()

    # Save which page to display next
    print("Page:" + str(parameterinfo["page"]))
    next_page = parameterinfo["page"]
    print(request.session['page_nr'])

    if next_page > int(request.session['page_nr']):
        request.session['page_nr'] = next_page

        # Save progressbar status
        progress = parameterinfo["progress"]
        request.session['progress'] = progress

        saveTime(request, next_page)

        return HttpResponse(200)

    else:
        print("Differing page_nr")

        response = HttpResponse()
        response.status_code = 400
        return response


# Save personal info from frontend in DB
@ensure_csrf_cookie
def saveData(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveData" + " " + str(
            parameterinfo) + "\n")
        f.close()

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
                submission.framing = request.session.get('rand')
                submission.save()
            else:
                print("Already saved terms_agree info. No changes made to DB.")

        # Save if participants personal info
        if parameterinfo["type"] == 'personal':
            if Submission.objects.filter(session=session, age__isnull=True) and \
                    Submission.objects.filter(session=session, gender__isnull=True):
                age = parameterinfo["age"]
                gender = parameterinfo["gender"]
                submission = Submission.objects.get(session=session)
                submission.age = age
                submission.gender = gender
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
                submission.save()
                print("saveFinish")
            else:
                print("Already saved finished info. No changes made to DB.")

    else:
        print("ERROR: Submission does not exist.")

    return HttpResponse(200)


# Calculate actual score for each participant
def calculateScore(request, task):
    score_pre = 0
    score_main = 0
    score_extra = 0

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    if task == "p2":
        answers_p1 = TaskSubmission.objects.filter(session=session, type='p1')
        answers_p2 = TaskSubmission.objects.filter(session=session, type='p2')

        for answer_p1 in answers_p1:
            task_id = answer_p1.task_id
            correct_answer = AnswerChoice.objects.get(task=task_id, correct_answer=True)
            if answer_p1.answer == correct_answer.text:
                score_pre += 1

        for answer_p2 in answers_p2:
            task_id = answer_p2.task_id
            correct_answer = AnswerChoice.objects.get(task=task_id, correct_answer=True)
            if answer_p2.answer == correct_answer.text:
                score_pre += 1

        print("Pre tasks score: " + str(score_pre))

        if submission_exist:
            submission = Submission.objects.get(session=session)

            task_score = TaskScore()
            task_score.session = session
            task_score.submission = submission
            task_score.score_pre = score_pre
            task_score.save()

    if task == "m2":
        answers_m1 = TaskSubmission.objects.filter(session=session, type='m1')
        answers_m2 = TaskSubmission.objects.filter(session=session, type='m2')

        for answer_m1 in answers_m1:
            task_id = answer_m1.task_id
            correct_answer = AnswerChoice.objects.get(task=task_id, correct_answer=True)
            if answer_m1.answer == correct_answer.text:
                score_main += 1

        for answer_m2 in answers_m2:
            task_id = answer_m2.task_id
            correct_answer = AnswerChoice.objects.get(task=task_id, correct_answer=True)
            if answer_m2.answer == correct_answer.text:
                score_main += 1

        print("Main tasks score: " + str(score_main))

        if submission_exist:
            submission = Submission.objects.get(session=session)

            task_score = TaskScore.objects.get(session=session)
            task_score.score_main = score_main
            task_score.save()

    if task == "extraTask":
        answers_extra = ExtraTaskSubmission.objects.filter(session=session)

        for answer_extra in answers_extra:
            task_id = answer_extra.task_id
            correct_answer = ExtraAnswerChoice.objects.get(task=task_id, correct_answer=True)
            if answer_extra.answer == correct_answer.text:
                score_extra += 1

        print("Extra tasks score: " + str(score_extra))

        if submission_exist:
            submission = Submission.objects.get(session=session)

            task_score = TaskScore.objects.get(session=session)
            task_score.score_extra = score_extra
            task_score.save()


# Save tasks answers from frontend in DB
@ensure_csrf_cookie
def saveTask(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveTask" + " " + str(
            parameterinfo) + "\n")
        f.close()

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()
    request_delete = Submission.objects.get(session=session).request_delete
    par_type = parameterinfo["type"]

    if submission_exist and not request_delete:
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

        if par_type == "p2" or par_type == "m2":
            calculateScore(request, par_type)

    return HttpResponse(200)


# Save answers from extra tasks
@ensure_csrf_cookie
def saveExtraTask(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)
    par_id = parameterinfo["id"]

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveExtraTask" + " " + str(
            parameterinfo) + "\n")
        f.close()

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()
    request_delete = Submission.objects.get(session=session).request_delete

    if submission_exist and not request_delete:
        if not ExtraTaskSubmission.objects.filter(session=session, task_id=par_id).exists():
            task_sub = ExtraTaskSubmission()
            task_sub.submission = Submission.objects.get(session=session)
            task_sub.session = session
            task_sub.task_id = par_id
            task_sub.answer = parameterinfo["answer"]

            task_sub.save()

        else:
            print("Already saved extra task with id " + str(par_id) + ". No changes made to DB.")

        calculateScore(request, "extraTask")

    return HttpResponse(200)


# Save answers of Questionnaires from frontend in DB
@ensure_csrf_cookie
def saveQuestionnaire(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveQuestionnaire" + " " + str(
            parameterinfo) + "\n")
        f.close()

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()
    request_delete = Submission.objects.get(session=session).request_delete
    par_type = parameterinfo["name"]
    par_name = parameterinfo["type"]

    if submission_exist and not request_delete:
        listitem = parameterinfo["listarray"]
        for item in listitem:
            question_item = item["item"]
            question_id = item["question_id"]
            if not QuestionnaireSubmission.objects.filter(session=session, name=par_name, type=par_type,
                                                          item=question_item).exists():
                question_sub = QuestionnaireSubmission()
                question_sub.submission = Submission.objects.get(session=session)
                question_sub.session = session

                question_sub.name = par_name
                question_sub.type = par_type

                question_sub.item = question_item
                question_sub.question_id = Question.objects.get(pk=question_id)
                question_sub.answer = item["answer"]

                question_sub.save()

            else:
                print("Already saved questionnaire " + str(par_name) + " info of type:" + str(par_type) + ", item:" +
                      str(question_item) + ". No changes made to DB.")

    return HttpResponse(200)


# Delete data of participant on request
@ensure_csrf_cookie
def deleteData(request):
    print("delete")
    finish = finishedStudy(request)
    if finish is True:
        return render(request, 'finish.html')
    print("Participant " + request.session.session_key + " wants to delete their data")

    f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
    f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "deleteData" + "\n")
    f.close()

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    if submission_exist:
        submission = Submission.objects.get(session=session)
        submission.request_delete = bool(True)
        submission.save()

    # Delete Task and Questionniare submissions
    TaskSubmission.objects.filter(session=session).delete()
    QuestionnaireSubmission.objects.filter(session=session).delete()

    # TODO delete whole IF
    # request.session.flush()
    # request.session['page_nr'] = 0
    # page_nr = request.session['page_nr']
    # request.session['progress'] = 0
    # progress = request.session['progress']
    return HttpResponse(200)


# Save input of textfield on last card
@ensure_csrf_cookie
def saveDeceptionInput(request):
    getparameterinfo = request.body.decode('utf-8')
    parameterinfo = json.loads(getparameterinfo)

    if parameterinfo is not None:
        f = open('logs/log_' + str(request.session.session_key) + '.txt', 'a+')
        f.write(str(time.ctime()) + " " + str(request.session.session_key) + " " + "saveDeception" + " " + str(
            parameterinfo) + "\n")
        f.close()

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()
    par_text = parameterinfo["text"]
    suspect = parameterinfo["suspect"]

    if submission_exist:
        if Submission.objects.filter(session=session, suspect_deception__isnull=True):
            submission = Submission.objects.get(session=session)
            submission.suspect_deception = bool(strtobool(suspect))
            submission.text_deception = par_text
            submission.save()
            print("saveDeception")
        else:
            print("Already saved deception input on last card. ")

    return HttpResponse(200)


# Get scores for participant to display on end card
def getScore(request):
    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    if submission_exist:
        if TaskScore.objects.filter(session=session):
            task_score = TaskScore.objects.get(session=session)

            answers_extra = ExtraTaskSubmission.objects.filter(session=session)
            print(session)
            print(answers_extra)
            print(answers_extra.exists())

            if answers_extra.exists():
                count = answers_extra.count()

                data = json.dumps({'pre': task_score.score_pre, 'main': task_score.score_main,
                                   'extra': task_score.score_extra, 'count': count})

            else:
                data = json.dumps({'pre': task_score.score_pre, 'main': task_score.score_main})

            return HttpResponse(data)

    return HttpResponse(json.dumps({'pre': '-', 'main': '-'}))


# Check if participant has already finished study
def finishedStudy(request):
    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    data = False

    if submission_exist:
        if Submission.objects.filter(session=session):
            submission = Submission.objects.get(session=session)
            data = submission.finished

    return data


# Save time spend for each website
def saveTime(request, next_page):
    # print("On page" + str(next_page))
    # print(time.time())
    # print(time.ctime(time.time()))

    session = Session.objects.get(session_key=request.session.session_key)
    submission_exist = Submission.objects.filter(session=session).exists()

    if submission_exist:
        if Submission.objects.filter(session=session):
            var_time = TimeSpend()
            var_time.submission = Submission.objects.get(session=session)
            var_time.session = session
            var_time.page_nr = next_page
            var_time.start_time = time.time()

            var_time.save()


# Eval Backend for admin
def evaluation(request):
    if request.user.is_superuser:
        submissions = Submission.objects.filter(terms_agree=True, finished=True, request_delete=False)
        return render(request, 'eval.html', context={"submissions": submissions})
    else:
        print('Access denied. You are not logged in as superuser.')
        return HttpResponseRedirect(reverse('index'))


def showParticipant(request, submission_id):
    questionnaire = []
    task = []
    questions = Question.objects.all()
    if request.user.is_superuser:
        if Submission.objects.filter(pk=submission_id).exists():
            submission = Submission.objects.get(pk=submission_id)
            if QuestionnaireSubmission.objects.filter(submission=submission).exists():
                questionnaire_sub = QuestionnaireSubmission.objects.filter(submission=submission)
                for q_sub in questionnaire_sub:
                    questionnaire.append(q_sub)
            else:
                questionnaire.append("--")
            if TaskSubmission.objects.filter(submission=submission).exists():
                task_sub = TaskSubmission.objects.filter(submission=submission)
                for t_sub in task_sub:
                    task.append(t_sub)
            else:
                task.append("--")
            if TaskScore.objects.filter(submission=submission).exists():
                score = TaskScore.objects.get(submission=submission)
            else:
                score = ""
            return render(request, 'show_participant.html', context={'submission': submission, 'questionnaire':
                questionnaire, 'task': task, 'score': score, 'questions': questions})
        else:
            print('Submission ' + str(submission_id) + ' does not exist or has not accepted the terms .')
            return HttpResponseRedirect(reverse('eval'))
    else:
        print('Access denied. You are not logged in as superuser.')
        return HttpResponseRedirect(reverse('index'))


def exportCSV(request):
    if request.user.is_superuser:

        with open('exports/submission_score.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            header = ['pk', 'session', 'framing', 'age', 'gender', 'list_p1', 'list_p2', 'list_m1', 'list_m2',
                      'suspect_deception', 'text_deception', 'taskscore__score_pre', 'taskscore__score_main']

            # write the header
            writer.writerow(header)

            # write the data
            submissions = Submission.objects.filter(terms_agree=True, finished=True, request_delete=False).values_list(
                'pk', 'session', 'framing', 'age', 'gender', 'list_p1', 'list_p2', 'list_m1', 'list_m2',
                'suspect_deception', 'text_deception', 'taskscore__score_pre', 'taskscore__score_main')

            for submission in submissions:
                writer.writerow(submission)

        with open('exports/questionnaires.csv', 'w', encoding='UTF8') as q:
            writer = csv.writer(q)

            header = ['session', 'name', 'type', 'item', 'question_id', 'answer']

            # write the header
            writer.writerow(header)

            # write the data
            questions = QuestionnaireSubmission.objects.filter(submission__terms_agree=True, submission__finished=True,
                                                               submission__request_delete=False).values_list(
                'session', 'name', 'type', 'item', 'question_id', 'answer')

            for question in questions:
                writer.writerow(question)

        with open('exports/tasks.csv', 'w', encoding='UTF8') as t:
            writer = csv.writer(t)

            header = ['session', 'type', 'item', 'task_id', 'answer']

            # write the header
            writer.writerow(header)

            # write the data
            tasks = TaskSubmission.objects.filter(submission__terms_agree=True, submission__finished=True,
                                                  submission__request_delete=False).values_list(
                'session', 'type', 'item', 'task_id', 'answer')

            for task in tasks:
                writer.writerow(task)

        with open('exports/time.csv', 'w', encoding='UTF8') as ti:
            writer = csv.writer(ti)

            header = ['session', 'page_nr', 'start_time']

            # write the header
            writer.writerow(header)

            # write the data
            timeslots = TimeSpend.objects.filter(submission__terms_agree=True, submission__finished=True,
                                                 submission__request_delete=False).values_list(
                'session', 'page_nr', 'start_time')

            for timeslot in timeslots:
                writer.writerow(timeslot)

        return HttpResponseRedirect(reverse('eval'))
    else:
        print('Access denied. You are not logged in as superuser.')
        return HttpResponseRedirect(reverse('index'))


def individualCSV(request, submission_id):
    if request.user.is_superuser:

        filename_f = "exports/submission_score_" + str(submission_id) + ".csv"
        with open(filename_f, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            header = ['pk', 'session', 'framing', 'age', 'gender',
                      'suspect_deception', 'text_deception', 'taskscore__score_pre', 'taskscore__score_main']
            # 'list_p1', 'list_p2', 'list_m1', 'list_m2',

            # write the header
            writer.writerow(header)

            # write the data
            submissions = Submission.objects.filter(pk=submission_id, terms_agree=True, finished=True,
                                                    request_delete=False).values_list(
                'pk', 'session', 'framing', 'age', 'gender',
                'suspect_deception', 'text_deception', 'taskscore__score_pre', 'taskscore__score_main')

            for submission in submissions:
                writer.writerow(submission)

        filename_q = "exports/questionnaires_" + str(submission_id) + ".csv"
        with open(filename_q, 'w', encoding='UTF8') as q:
            writer = csv.writer(q)

            header = ['session', 'name', 'type', 'item', 'question_id', 'answer']

            # write the header
            writer.writerow(header)

            # write the data
            questions = QuestionnaireSubmission.objects.filter(submission=submission_id, submission__terms_agree=True,
                                                               submission__finished=True,
                                                               submission__request_delete=False).values_list(
                'session', 'name', 'type', 'item', 'question_id', 'answer')

            for question in questions:
                writer.writerow(question)

        filename_t = "exports/tasks_" + str(submission_id) + ".csv"
        with open(filename_t, 'w', encoding='UTF8') as t:
            writer = csv.writer(t)

            header = ['session', 'type', 'item', 'task_id', 'answer']

            # write the header
            writer.writerow(header)

            # write the data
            tasks = TaskSubmission.objects.filter(submission=submission_id, submission__terms_agree=True,
                                                  submission__finished=True,
                                                  submission__request_delete=False).values_list(
                'session', 'type', 'item', 'task_id', 'answer')

            for task in tasks:
                writer.writerow(task)

        filename_ti = "exports/time_" + str(submission_id) + ".csv"
        with open(filename_ti, 'w', encoding='UTF8') as ti:
            writer = csv.writer(ti)

            header = ['session', 'page_nr', 'start_time']

            # write the header
            writer.writerow(header)

            # write the data
            timeslots = TimeSpend.objects.filter(submission=submission_id, submission__terms_agree=True,
                                                 submission__finished=True,
                                                 submission__request_delete=False).values_list(
                'session', 'page_nr', 'start_time')

            for timeslot in timeslots:
                writer.writerow(timeslot)

        return HttpResponseRedirect(reverse('eval'))
    else:
        print('Access denied. You are not logged in as superuser.')
        return HttpResponseRedirect(reverse('index'))
