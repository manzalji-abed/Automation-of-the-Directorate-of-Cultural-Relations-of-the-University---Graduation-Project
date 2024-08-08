import datetime
# import pythoncom
import time
# import win32com.client
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.core import serializers as ser
from django.contrib import messages
from django.apps import apps
from django.db.models import Q, Max
from django.middleware.csrf import get_token
from json import dumps, loads, dump, load
from dateutil.relativedelta import relativedelta
from .models import *
from .forms import *
from .serializers import *
from . import forms
from . import serializers
from ast import literal_eval
from .constantVariables import ADJECTIVE_CHOICES
from rest_framework.serializers import Serializer



import os.path
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from django.shortcuts import render
from .forms import UploadFileForm
from django.http import FileResponse

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


@login_required(login_url='app:login')
def UploadFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # If a custom filename is provided, use it. Otherwise, use the original filename.
            custom_filename = form.cleaned_data.get('custom_filename') or "synchronization"
            # Create a new UploadedFile object and save it to the database
            uploaded=request.FILES['file']
            uploaded._name="synchronization.json"
            uploaded_file = UploadedFile(file=uploaded, filename=custom_filename)
            uploaded_file.save()
            return render(request, 'home/success.html')
    else:
        form = UploadFileForm()
    return render(request, 'home/upload.html', {'form': form})


@login_required(login_url='app:login')
def DownloadFile(request):
    response = FileResponse(open("uploads/synchronization.json", 'rb'))
    response['Content-Disposition'] = 'attachment; filename=' + "synchronization.json"
    response['Content-Type'] = 'application/octet-stream'
    return response


@login_required(login_url='app:login')
def RemoveOldToken():
    N = 6
    
    
    list_of_files = os.listdir()
    
    current_time = time.time()
    
    day = 86400
    if(len(list_of_files)>0):
        for i in list_of_files:
            file_location = os.path.join(os.getcwd(), i)
            file_time = os.stat(file_location).st_mtime
        
            if(file_time < current_time - day*N):
                if 'token' in file_location:
                    print(f" Delete : {i}")
                    os.remove(file_location)


@login_required(login_url='app:login')
def SendEmailHotmail(email,subject,message):
    ol=win32com.client.Dispatch("outlook.application",pythoncom.CoInitialize())
    olmailitem=0x0 
    newmail=ol.CreateItem(olmailitem)
    newmail.Subject= subject
    newmail.To=email
    newmail.CC=email
    newmail.Body=message
    newmail.Send()


@login_required(login_url='app:login')
def SendEmailGmail(email,subject,message):
    RemoveOldToken()
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'GGG.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        emails=[]
        emails_str=""

        todayDate = datetime.date.today() 
        lateDate = datetime.date.today() + relativedelta(months=-3)
        reports = Report.objects.filter().values('dispatchDecisionId_id').annotate(Max('reportDate')).filter(Q(**{'reportDate__max__lte':todayDate})).values('dispatchDecisionId_id')
        print(reports)
        dis =[]
        for report in list(reports):
            dis.append(report['dispatchDecisionId_id'])
        dispatchLate= Dispatch.objects.filter(Q(**{'id__in': dis}) & Q(**{'dispatchEndDate__gte' : todayDate})).values('studentId_id')
        res =[]
        for dispatch in list(dispatchLate):
            res.append(dispatch['studentId_id'])
        
        late = list(Demonstrator.objects.filter(pk__in=res).values('email'))

        for x in range(len(late)):
                if late[x]['email']:
                    if late[x]['email'] not in emails:
                        emails.append(late[x]['email'])

        for x in emails:
            emails_str+=x+" "

        

        emails_str=emails_str[:-2]

        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(message)
        message['to'] = email
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


@login_required(login_url='app:login')
def SendEmails(request):
    if request.POST['emails'] == 'normal':
        try:
            emails=[]
            if request.POST['email']:
                emails.append(request.POST['email'])

            if request.POST['user']:
                emails.append(request.POST['user']+"@albaath-univ.edu.sy")

            if request.POST['college'] == 'all':

                all=list(Demonstrator.objects.all().filter().values('email'))

                for x in range(len(all)):
                    if all[x]['email']:
                        if all[x]['email'] not in emails:
                            emails.append(all[x]['email'])

                
            elif request.POST['college'] is not None:
                print(request.POST['college'])
                college = list(Demonstrator.objects.filter(college=request.POST['college']).values('email'))
                for x in range(len(college)):
                    if college[x]['email']:
                        if college[x]['email'] not in emails:
                            emails.append(college[x]['email'])

            

            emails_str=""

            for x in emails:
                emails_str+=x+", "
                if request.POST['server'] == 'gmail':
                    SendEmailGmail(x,request.POST['subject'],request.POST['msg'])
                elif request.POST['server'] == 'hotmail':
                    SendEmailHotmail(x,request.POST['subject'],request.POST['msg'])

            emails_str=emails_str[:-2]


        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')


        return render(request, 'home/success.html', {"emails": emails})

    elif request.POST['emails'] == 'late':
        emails=[]
        emails_str=""

        todayDate = datetime.date.today() 
        lateDate = datetime.date.today() + relativedelta(seconds=-5)
        reports = Report.objects.filter().values('dispatchDecisionId_id').annotate(Max('reportDate')).filter(Q(**{'reportDate__max__lte':lateDate})).values('dispatchDecisionId_id')
        dis =[]
        for report in list(reports):
            dis.append(report['dispatchDecisionId_id'])
        dispatchLate= Dispatch.objects.filter(Q(**{'id__in': dis})).values('studentId_id')
        res =[]
        for dispatch in list(dispatchLate):
            res.append(dispatch['studentId_id'])
        
        late = list(Demonstrator.objects.filter(pk__in=res).values('email'))
        print(late)
        for x in range(len(late)):
                if late[x]['email']:
                    if late[x]['email'] not in emails:
                        emails.append(late[x]['email'])

        for x in emails:
            emails_str+=x+", "
            message="تم انتهاء المدة القانونية الخاصة بك يطلب اليك بالسرعة القصوى ارسال تقرير دراسي مفصل...."
            if request.POST['server'] == 'gmail':
                SendEmailGmail(x,"إنذار",message)
            elif request.POST['server'] == 'hotmail':
                SendEmailHotmail(x,"إنذار",message)

        emails_str=emails_str[:-2]

        return render(request, 'home/success.html', {"emails": emails})


@login_required(login_url='app:login')
def Email(request):
    # permissions= ser.serialize('json', Permissions.objects.all(),fields=('permissionsCollege'))
    permissions=list(Permissions.objects.all().values('permissionsCollege'))
    d = JsonResponse({"data": permissions})
    strr = d.content.decode("utf-8")
    return render(request, 'home/send_email.html',{"select": strr})


@login_required(login_url='app:login')
def Register(request):

    if request.method == 'POST':
        if request.user.is_superuser:
            user = User.objects.create_user(
                username=request.POST['username'],
                first_name=request.POST['firstName'],
                last_name=request.POST['lastName'],
                password=request.POST['password'],
                email=request.POST['email']
            )
            for perm in request.POST.getlist('permissions'):
                permission, created= Permissions.objects.get_or_create(permissionsCollege=perm)
                user.permissions.add(permission.id)
            LastPull.objects.create(userId= user)
            messages.add_message(request, messages.SUCCESS,"أهلاً و سهلاً")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تسجيل موظفين")
            return redirect('app:home')

    if request.user.is_superuser:
        # permissions= ser.serialize('json', Permissions.objects.all(),fields=('permissionsCollege'))
        permissions=list(Permissions.objects.filter().values('permissionsCollege'))
        d = JsonResponse({"data": permissions})
        strr = d.content.decode("utf-8")
        
        return render(request, 'registration/register.html', {'colleges': strr })
    else:
        return render(request, 'registration/result.html', {'result': 'denied'})


def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,"أهلاً و سهلاً")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"اسم المستخدم أو كلمة المرور خاطئة")
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


@login_required(login_url='app:login')
def Logout(request):
    logout(request)
    messages.add_message(request, messages.ERROR,"تم تسجيل الخروج")
    return redirect('app:home')


@login_required(login_url='app:login')
def CalculateDispatchEndDate(dispatch):
    dateItem= datetime.datetime.strptime(dispatch[0]['commencementDate'], '%Y-%m-%d').date()
    endDate= dateItem
    durationChangeLength= len(dispatch[0]['durationChange'])
    if durationChangeLength:
        day = dispatch[0]['durationChange'][durationChangeLength-1]['durationChangeDurationDay']
        month = dispatch[0]['durationChange'][durationChangeLength-1]['durationChangeDurationMonth']
        year = dispatch[0]['durationChange'][durationChangeLength-1]['durationChangeDurationYear']
        endDate+= relativedelta(days=day) + relativedelta(months=month) + relativedelta(years=year)
    else:
        day = dispatch[0]['dispatchDurationDay']
        month = dispatch[0]['dispatchDurationMonth']
        year = dispatch[0]['dispatchDurationYear']
        endDate+= relativedelta(days=day) + relativedelta(months=month) + relativedelta(years=year) 
    day = dispatch[0]['languageCourseDurationDay']
    month = dispatch[0]['languageCourseDurationMonth']
    year = dispatch[0]['languageCourseDurationYear']
    endDate+= relativedelta(days=day) + relativedelta(months=month) + relativedelta(years=year) 
    for extension in dispatch[0]['extension']:
        day = extension['extensionDurationDay']
        month = extension['extensionDurationMonth']
        year = extension['extensionDurationYear']
        endDate+= relativedelta(days=day) + relativedelta(months=month) + relativedelta(years=year)
    for freeze in dispatch[0]['freeze']:
        day = freeze['freezeDurationDay']
        month = freeze['freezeDurationMonth']
        year = freeze['freezeDurationYear']
        endDate+= relativedelta(days=day) + relativedelta(months=month) + relativedelta(years=year)

    return endDate


@login_required(login_url='app:login')
def generalInsert(request, mainField, baseDic, model, addModel, savePoint):
    id = None
    for i in range(len(request.POST.getlist(mainField))):
        dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
        dic.update(baseDic)
        dic.update({'isOffline': True})
        for field in model._meta.local_fields:
            if field.name in request.POST:
                dic[field.name] = request.POST.getlist(field.name)[i]
        form = addModel(dic)
        if form.is_valid():
            id = form.save()
        else:
            transaction.savepoint_rollback(savePoint)
            print(form.errors)
            return form.errors
    return id


@login_required(login_url='app:login')
def DemonstratorInsert2(request):
    if request.method == 'POST':
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if request.POST['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                demonId = generalInsert(request, 'name', {}, Demonstrator, AddDemonstrator, savePoint)
                if type(demonId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:insert')

                id = generalInsert(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:insert')

                id = generalInsert(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:insert')

                id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:insert')

                id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة المعيد")
                    return redirect('app:insert')
                

            messages.add_message(request, messages.SUCCESS,"تم تسجيل المعيد")
            return redirect('app:insert')
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:insert')

    else:
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        return render(request, 'home/insert.html', {'permissions': permissionList})


@login_required(login_url='app:login')
def GraduateStudiesDegreeInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة الشهادة")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تمت إضافة الشهادة")
            return redirect('app:demonstrator', id= demonId)
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)

    else:
        return render(request, 'home/insert.html')


@login_required(login_url='app:login')
def CertificateExcellenceYearInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة الشهادة")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تمت إضافة الشهادة")
            return redirect('app:demonstrator', id= demonId)
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)

    else:
        return render(request, 'home/insert.html')


@login_required(login_url='app:login')
def AdjectiveChangeInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الصفة")
                    return redirect('app:home')

                demonstrator = Demonstrator.objects.get(pk=demonId)
                demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
                Demonstrator.full_clean(self=demonstrator)
                Demonstrator.save(self=demonstrator)

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الصفة")
            return redirect('app:home')
        else: 
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')

    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def DispatchInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():

                savePoint = transaction.savepoint()

                dispatchId = generalInsert(request, 'dispatchDecisionNumber', {'studentId': demonId }, Dispatch, AddDispatch, savePoint)
                if type(dispatchId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة الإيفاد")
                    return redirect('app:demonstrator', id= demonId)

                id = generalInsert(request, 'regularizationDecisionNumber', {'regularizationDecisionId': dispatchId}, Regularization, AddRegularization, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة الإيفاد")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تم إضافة الإيفاد")
            return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)

    else:
        d = Demonstrator.objects.get(pk=demonId)
        return render(request, 'home/insert-dispatch.html', {"d":d})


@login_required(login_url='app:login')
def getDispatch(request, dispatchId):
    ans = Dispatch.objects.get(pk = dispatchId)
    return render(request, 'home/show-dispatch.html', {'dispatch': ans})


@login_required(login_url='app:login')
def ReportInsert(request, dispatchId, demonId):
    
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                reportId = generalInsert(request, 'report', {'dispatchDecisionId': dispatchId}, Report, AddReport, savePoint)
                if type(reportId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التقرير")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تم إضافة التقرير ")
            return redirect('app:demonstrator', id= demonId)
            
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:reportinsert')


@login_required(login_url='app:login')
def ExtensionInsert(request, dispatchId,demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college', 'studentId__name', 'studentId__fatherName','studentId__email','dispatchEndDate'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                extensionId = generalInsert(request, 'extensionDecisionNumber', {'dispatchDecisionId': dispatchId}, Extension, AddExtension, savePoint)
                if type(extensionId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التمديد")
                    return redirect('app:demonstrator', id= demonId)
                
                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التمديد")
                    return redirect('app:demonstrator', id= demonId)

                informationForEmail={ 'name': college[0]['studentId__name'],
                                    'fatherName': college[0]['studentId__fatherName'],
                                    'extensionDecisionNumber': request.POST['extensionDecisionNumber'],
                                    'extensionDecisionDate': request.POST['extensionDecisionDate'],
                                    'extensionDecisionType': request.POST['extensionDecisionType'],
                                    'extensionDurationYear': request.POST['extensionDurationYear'],
                                    'extensionDurationMonth': request.POST['extensionDurationMonth'],
                                    'extensionDurationDay': request.POST['extensionDurationDay'],
                                    }
            messages.add_message(request, messages.SUCCESS,"تم إضافة التمديد ")
            return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)
    else:
        return render(request, 'home/ext.html')


@login_required(login_url='app:login')
def FreezeInsert(request, dispatchId,demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                freezeId = generalInsert(request, 'freezeDecisionNumber', {'dispatchDecisionId': dispatchId}, Freeze, AddFreeze, savePoint)
                if type(freezeId) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التجميد")
                    return redirect('app:demonstrator', id= demonId)
                
                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة التجميد")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تم إضافة التجميد ")
            return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)
    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def DurationChangeInsert(request, dispatchId, demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'durationChangeDurationYear', {'dispatchDecisionId': dispatchId}, DurationChange, AddDurationChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير المدة")
                    return redirect('app:demonstrator', id= demonId)
                
                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير المدة")
                    return redirect('app:demonstrator', id= demonId)

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير المدة ")
            return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)
        
    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def AlimonyChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newAlimony', {'dispatchDecisionId': dispatchId}, AlimonyChange, AddAlimonyChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير النفقة")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير النفقة ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def UniversityChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newUniversity', {'dispatchDecisionId': dispatchId}, UniversityChange, AddUniversityChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الجامعة")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الجامعة ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def SpecializationChangeInsert(request, dispatchId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                id = generalInsert(request, 'newSpecialization', {'dispatchDecisionId': dispatchId}, SpecializationChange, AddSpecializationChange, savePoint)
                if type(id) == ErrorDict: 
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم يتم إضافة تغيير الاختصاص")
                    return redirect('app:home')

            messages.add_message(request, messages.SUCCESS,"تم إضافة تغيير الاختصاص ")
            return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:home')
        
    else:
        return render(request, 'registration/dispathInsert.html')


@login_required(login_url='app:login')
def getAllDemonstrators(request):
    data2 = ser.serialize('json', Demonstrator.objects.filter().all(), fields=('id', 'name', 'fatherName', 'motherName', 'college', 'university', "specialization"))
    return render(request, 'home/allDemonstrators.html', {'result': data2})


@login_required(login_url='app:login')
def getDemonstrator(request, id):
    demonstrator = Demonstrator.objects.select_related().prefetch_related().all().get(pk=id )
    permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
    return render(request, 'home/demonstrator.html', {'demonstrator': demonstrator, 'permissions': permissionList})
   

@login_required(login_url='app:login')
def GetAllEmails(request):
    if request.method == 'POST':
        all = Demonstrator.objects.filter().values('email', 'mobile', 'name')
        print(all)
        return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def GetLateEmails(request):
    if request.method == 'POST':
        todayDate = datetime.date.today() 
        lateDate = datetime.date.today() + relativedelta(months=-3)
        reports = Report.objects.filter().values('dispatchDecisionId_id').annotate(Max('reportDate')).filter(Q(**{'reportDate__max__lte':todayDate})).values('dispatchDecisionId_id')
        dis =[]
        for report in list(reports):
            dis.append(report['dispatchDecisionId_id'])
        dispatchLate= Dispatch.objects.filter( Q(**{'id__in': dis}) & Q(**{'dispatchEndDate__gte' : todayDate})).values('studentId_id')
        res =[]
        for dispatch in list(dispatchLate):
            res.append(dispatch['studentId_id'])
        
        late = Demonstrator.objects.filter(pk__in=res ).values('email', 'mobile', 'name')
        print(late)
        return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def GetCollegeEmails(request):
    if request.method == 'POST':
        college = Demonstrator.objects.filter(college=request.POST['college']).values('email', 'mobile', 'name')
        print(college)
        return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def generalUpdate(request, mainField, baseDic, model, addModel, obj, savePoint):
    try:
        id = None
        if mainField in request.POST:
            dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
            dic.update(baseDic)
            for field in model._meta.local_fields:
                if field.name in request.POST:
                    dic[field.name] = request.POST[field.name]
            form = addModel(dic, instance=obj)
            if form.is_valid():
                id = form.save()
            else:
                transaction.savepoint_rollback(savePoint)
                print(form.errors)
                return form.errors
        return id
    except:
        print('error')


@login_required(login_url='app:login')
def UpdateDemonstrator(request, id):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=id).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                demonstrators = Demonstrator.objects.filter(pk=id)
                for demonstrator in demonstrators:
                    demonId= generalUpdate(request, 'name', {}, Demonstrator, AddDemonstrator, demonstrator, savePoint)
                    if type(demonId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateUniversityDegree(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                universityDegrees= UniversityDegree.objects.filter(pk=id)
                for universityDegree in universityDegrees:
                    resId = generalUpdate(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, universityDegree, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateNomination(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                nominations= Nomination.objects.filter(pk=id)
                for nomination in nominations:
                    resId = generalUpdate(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, nomination, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateAdjectiveChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                adjectiveChange= AdjectiveChange.objects.filter(pk=id)
                for model in adjectiveChange:
                    resId = generalUpdate(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrators= Demonstrator.objects.filter(pk=demonId)
                        for demonstrator in demonstrators:
                            demonstrator.currentAdjective = demonstrator['adjectiveChange'][len(demonstrator['adjectiveChange'])-1]
                            Demonstrator.full_clean(self=demonstrator)
                            Demonstrator.save(self=demonstrator)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateCertificateOfExcellence(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                certificateOfExcellence= CertificateOfExcellence.objects.filter(pk=id)
                for model in certificateOfExcellence:
                    resId = generalUpdate(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateGraduateStudies(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                graduateStudies= GraduateStudies.objects.filter(pk=id)
                for model in graduateStudies:
                    resId = generalUpdate(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateDispatch(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                dispatchs= Dispatch.objects.filter(pk=id)
                for dispatch in dispatchs:
                    dispatchId = generalUpdate(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, dispatch, savePoint)
                    if type(dispatchId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    dispatchObject = Dispatch.objects.filter(pk=id)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})
                

            return JsonResponse({"status": "good" , 'endDate': endDate})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateReport(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                reports= Report.objects.filter(pk=id)
                for report in reports:
                    resId = generalUpdate(request, 'regularizationDecisionNumber', {'dispatchDecisionId': report.dispatchDecisionId}, Report, AddReport, report, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateRegularization(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                regularizations= Regularization.objects.filter(pk=id)
                for regularization in regularizations:
                    resId = generalUpdate(request, 'regularizationDecisionNumber', {'regularizationDecisionId': regularization.regularizationDecisionId}, Regularization, AddRegularization, regularization, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateExtension(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                extensions= Extension.objects.filter(pk=id)
                dispatchId = -1
                for extension in extensions:
                    dispatchId= extension.dispatchDecisionId
                    extensionId = generalUpdate(request, 'extensionDecisionNumber', {'dispatchDecisionId': extension.dispatchDecisionId}, Extension, AddExtension, extension, savePoint)
                    if type(extensionId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateFreeze(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                freezes= Freeze.objects.filter(pk=id)
                dispatchId=-1
                for freeze in freezes:
                    dispatchId= freeze.dispatchDecisionId
                    freezeId = generalUpdate(request, 'freezeDecisionNumber', {'dispatchDecisionId': freeze.dispatchDecisionId}, Freeze, AddFreeze, freeze, savePoint)
                    if type(freezeId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateDurationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                durationChange= DurationChange.objects.filter(pk=id)
                dispatchId=-1
                for model in durationChange:
                    dispatchId=model.dispatchDecisionId
                    resId = generalUpdate(request, 'durationChangeDurationYear', {'dispatchDecisionId': model.dispatchDecisionId}, DurationChange, AddDurationChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

                try:
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateAlimonyChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                alimonyChange= AlimonyChange.objects.filter(pk=id)
                for model in alimonyChange:
                    resId = generalUpdate(request, 'newAlimony', {'dispatchDecisionId': model.dispatchDecisionId}, AlimonyChange, AddAlimonyChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateUniversityChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                universityChange= UniversityChange.objects.filter(pk=id)
                for model in universityChange:
                    resId = generalUpdate(request, 'newUniversity', {'dispatchDecisionId': model.dispatchDecisionId}, UniversityChange, AddUniversityChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def UpdateSpecializationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                specializationChange= SpecializationChange.objects.filter(pk=id)
                for model in specializationChange:
                    resId = generalUpdate(request, 'newSpecialization', {'dispatchDecisionId': model.dispatchDecisionId}, SpecializationChange, AddSpecializationChange, model, savePoint)
                    if type(resId) == ErrorDict: return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})
 

@login_required(login_url='app:login')
def generalDelete(modelName, objectId):
    deletedObject= DeletedObjects()
    deletedObject.modelName= modelName
    deletedObject.objectId = objectId
    deletedObject.isOffline= True
    deletedObject.save()


@login_required(login_url='app:login')
def DeleteDemonstrator(request, id):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=id).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    demonstrators = Demonstrator.objects.filter(pk=id).delete()
                    generalDelete('Demonstrator', id) 
                except:
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteUniversityDegree(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityDegrees= UniversityDegree.objects.filter(pk=id).delete()
                    generalDelete('UniversityDegree', id)  
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteNomination(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    nominations= Nomination.objects.filter(pk=id).delete()
                    generalDelete('Nomination', id)
                except:
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteAdjectiveChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    adjectiveChange= AdjectiveChange.objects.filter(pk=id).delete()
                    generalDelete('AdjectiveChange', id)
                except:
                    return JsonResponse({"status": "bad"})


                try:
                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrators= Demonstrator.objects.filter(pk=demonId)
                        for demonstrator in demonstrators:
                            demonstrator.currentAdjective = demonstrator['adjectiveChange'][len(demonstrator['adjectiveChange'])-1]
                            Demonstrator.full_clean(self=demonstrator)
                            Demonstrator.save(self=demonstrator)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteCertificateOfExcellence(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    certificateOfExcellence= CertificateOfExcellence.objects.filter(pk=id).delete()
                    generalDelete('CertificateOfExcellence', id)
                except:
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteGraduateStudies(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    graduateStudies= GraduateStudies.objects.filter(pk=id).delete()
                    generalDelete('GraduateStudies', id)
                except:
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteDispatch(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                
                try:
                    dispatchs= Dispatch.objects.filter(pk=id).delete()
                    generalDelete('Dispatch', id)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})
                

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteReport(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    reports= Report.objects.filter(pk=id).delete()
                    generalDelete('Report', id)
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteRegularization(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    regularizations= Regularization.objects.filter(pk=id).delete()
                    generalDelete('Regularization', id)
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteExtension(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                try:
                    extensions2= Extension.objects.filter(pk=id)
                    dispatchId = -1
                    for extension in extensions2:
                        dispatchId= extension.dispatchDecisionId

                    extensions= Extension.objects.filter(pk=id).delete()
                    generalDelete('Extension', id)

                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteFreeze(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                try:
                    freezes2= Freeze.objects.filter(pk=id)
                    dispatchId=-1
                    for freeze in freezes2:
                        dispatchId= freeze.dispatchDecisionId

                    freezes= Freeze.objects.filter(pk=id).delete()
                    generalDelete('Freeze', id)

                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteDurationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()

                try:
                    durationChange2= DurationChange.objects.filter(pk=id)
                    dispatchId=-1
                    for model in durationChange2:
                        dispatchId=model.dispatchDecisionId

                    durationChange= DurationChange.objects.filter(pk=id).delete()
                    generalDelete('DurationChange', id)

                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    endDate = CalculateDispatchEndDate(dispatch)
                    for dispatchItem in dispatchObject:
                        dispatchItem.dispatchEndDate = endDate
                        Dispatch.full_clean(self=dispatchItem)
                        Dispatch.save(self=dispatchItem)
                except:
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteAlimonyChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    alimonyChange= AlimonyChange.objects.filter(pk=id).delete()
                    generalDelete('AlimonyChange', id)
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteUniversityChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityChange= UniversityChange.objects.filter(pk=id).delete()
                    generalDelete('UniversityChange', id)
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def DeleteSpecializationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    specializationChange= SpecializationChange.objects.filter(pk=id).delete()
                    generalDelete('SpecializationChange', id)
                except:
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": 'you are not allowed to edit in this college'})


@login_required(login_url='app:login')
def QueryDemonstrator(request):
    if request.method == 'POST':
        print(request.POST['cols'])
        
        
        def makeQuery(query, op):
            obj = Q()
            for item in query: 
                q = list(item.keys())[0]
                if type(item[q]) is list:
                    if op == 'or':
                        obj = obj | (makeQuery(item[q], q))
                    else:
                        obj = obj & (makeQuery(item[q], q))
                elif type(item[q]) is dict:
                    p = list (item[q].keys())[0]
                    if op == 'or':
                        if p =='__ne': obj = obj | ~Q(**{q: item[q][p]})
                        else: obj = obj | Q(**{q+p: item[q][p]})
                    else:
                        if p=='__ne': obj = obj & ~Q(**{q: item[q][p]})
                        else: Q(**{q+p: item[q][p]})
                else: 
                    if op == 'or':
                        obj = obj | Q(**{q: item[q]})
                    else: 
                        obj = obj & Q(**{q: item[q]})
                       
            return obj
        query = loads(request.POST['query'])
        print('q', query)
        op = list(query.keys())[0]
        obj = makeQuery(query[op], op)

        # result = list(Demonstrator.objects.select_related().prefetch_related().filter(obj))
        result2= Demonstrator.objects.filter(obj)
        da = SerializerDemonstrator(result2, many=True)
        print(da.data)
        finalResult={}
        if len(da.data):
            finalResult= loads(dumps(da.data))
            print(dumps(da.data[0]))
        
        # data= ser.serialize('json', result, fields=("id",*request.POST['cols'].split(',')))
        # print(data)

                        

        # result = Demonstrator.objects.select_related().prefetch_related().filter(obj).values("id",*request.POST['cols'].split(','))
        # print('res', result)
        print(finalResult)
        dat = JsonResponse({"data": finalResult})
        # print('dat', dat.content)
        stringgg = dat.content.decode('utf-8')
        # print('str', stringgg)
        print( request.POST['cols'].split(','))
        return render(request, "registration/result.html", {"result":stringgg, 'fields': request.POST['cols']})


@login_required(login_url='app:login')
def home(request):
    result={}
    result['allDemons'] = Demonstrator.objects.filter().count()
    todayDate= datetime.date.today() 
    result['allInDispatch'] = Dispatch.objects.filter(Q(**{'dispatchEndDate__gte': todayDate})).count()
    result['master'] = Dispatch.objects.filter(Q(**{'dispatchEndDate__gte': todayDate}) & Q(**{'requiredCertificate':'master'})).count()
    result['ph.d'] = Dispatch.objects.filter(Q(**{'dispatchEndDate__gte': todayDate}) & Q(**{'requiredCertificate':'ph.d'})).count()
    result['others'] = result['allDemons'] - result['master'] - result['ph.d']
    for adjective in ADJECTIVE_CHOICES:
        result[adjective[0]] = Demonstrator.objects.filter(currentAdjective= adjective[0]).count()
    result['phd'] = result['ph.d']
    result['returning_demonstrator'] = result['returning demonstrator']
    result['transfer_outside_the_university'] = result['transfer outside the university']
    result['end_services'] = result['end services']
    print(result)
    return render(request, 'home/home.html', {'statistics': result}) 


def Test(request):
    # date= request.user.lastPull.lastPullDate
    # data=[]
    # for model in apps.get_models():
    #     if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull']:
    #         tempData =list( model.objects.filter(lastModifiedDate__gte=date) )
    #         data.append( {'modelName': model.__name__, 'data':tempData})
    # todayDate = datetime.date.today() 
    # reports = Report.objects.filter().values('dispatchDecisionId_id').annotate(Max('reportDate')).filter(Q(**{'reportDate__max__lte':todayDate})).values('dispatchDecisionId_id')
    # print(reports)
    user = User.objects.get(pk=1)
    LastPull.objects.create(userId= user)
    # for model in apps.get_models():
    #     print(model.__name__)
    return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def goToHome(request):
    return redirect('app:home')


def getSerializer(modelName):
    
    if modelName == 'Permissions':
        return SerializerPermissions
    elif modelName == 'Demonstrator':
        return SerializerDemonstratorSingle
    elif modelName == 'UniversityDegree':
        return SerializerUniversityDegree
    elif modelName == 'Nomination':
        return SerializerNomination
    elif modelName == 'AdjectiveChange':
        return SerializerAdjectiveChange
    elif modelName == 'CertificateOfExcellence':
        return SerializerCertificateOfExcellence
    elif modelName == 'GraduateStudies':
        return SerializerGraduateStudies
    elif modelName == 'Dispatch':
        return SerializerDispatchSingle
    elif modelName == 'Report':
        return SerializerReport
    elif modelName == 'Regularization':
        return SerializerRegularization
    elif modelName == 'Extension':
        return SerializerExtension
    elif modelName == 'Freeze':
        return SerializerFreeze
    elif modelName == 'DurationChange':
        return SerializerDurationChange
    elif modelName == 'AlimonyChange':
        return SerializerAlimonyChange
    elif modelName == 'UniversityChange':
        return SerializerUniversityChange
    elif modelName == 'SpecializationChange':
        return SerializerSpecializationChange


@login_required(login_url='app:login')
def pullData(request):
    if request.method=='GET':
        if request.user.is_superuser:
             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    lastPullDate= request.user.lastPull.lastPullDate
                    data={}
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            serializerClass = getSerializer(model.__name__)
                            added = serializerClass(model.objects.filter(isOffline=True), many= True).data
                            updated =serializerClass(model.objects.filter(Q(lastModifiedDate__gte=lastPullDate) & ~Q(createdDate__gte=lastPullDate) ), many= True).data
                            deleted = SerializerDeletedObjects( DeletedObjects.objects.filter(modelName=model.__name__, createdDate__gte=lastPullDate), many= True).data
                            data.update( {model.__name__: {'updated':updated, 'added':added, 'deleted': deleted} })
                    # for delete all deleted archive
                    # deleteAll = DeletedObjects.objects.filter().delete()
                    print('data is: ',data)
                    with open('uploads/synchronization.json', 'w') as file:
                        dump(data, file, indent=None)
                        
                except Exception as e:
                    print(str(e))
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': 'done'}) 
            #  temp = LastPull.objects.filter(pk=1).update(lastPullDate=datetime.datetime.now)
             temp = LastPull.objects.get(pk=1)
             temp.lastPullDate=datetime.datetime.now
             temp.waitingMerge = True
             LastPull.save(self=temp)
             return render(request, 'registration/result.html', {'result': 'done'})
           


        else:
            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def generalPushAdd(request ,added, addModel, modelName, idMap, savePoint):
    id = None
    oldId = added['id']
    del added['id']
    dic = {'csrfmiddlewaretoken': get_token(request)}
    dic.update(added)
    dic.update({'isOffline': False})
    form = addModel(dic)
    if form.is_valid():
        id = form.save()
        if not idMap[modelName]:
            idMap[modelName] = {}
        idMap[modelName].update({oldId: id})
    else:
        transaction.savepoint_rollback(savePoint)
        return form.errors
    return id


@login_required(login_url='app:login')
def generalPushUpdate(request ,added, obj, addModel, savePoint):
    id = None
    dic = {'csrfmiddlewaretoken': get_token(request)}
    dic.update(added)
    dic.update({'isOffline': False})
    form = addModel(dic, instance=obj)
    if form.is_valid():
        id = form.save()
    else:
        transaction.savepoint_rollback(savePoint)
        return form.errors
    return id


def generalUpdateHub(request, added, obj, addModel, modelName, idMap, savePoint):
    #Demonstrator
    if modelName in ['Dispatch', 'GraduateStudies', 'CertificateOfExcellence', 'AdjectiveChange']:
        #studentId
        if idMap[modelName]:
            if idMap[modelName][added['studentId']]:
                added['studentId'] = idMap[modelName][added['studentId']]
    elif modelName == 'Nomination':
        #nominationDecision
        if idMap[modelName]:
            if idMap[modelName][added['nominationDecision']]:
                added['nominationDecision'] = idMap[modelName][added['nominationDecision']]
    elif modelName == 'UniversityDegree':
        #universityDegree
        if idMap[modelName]:
            if idMap[modelName][added['universityDegree']]:
                added['universityDegree'] = idMap[modelName][added['universityDegree']]

    #Dispatch
    elif modelName in ['Report', 'Extension', 'Freeze', 'DurationChange', 'AlimonyChange', 'UniversityChange', 'SpecializationChange']:
        #dispatchDecisionId
        if idMap[modelName]:
            if idMap[modelName][added['dispatchDecisionId']]:
                added['dispatchDecisionId'] = idMap[modelName][added['dispatchDecisionId']]
    elif modelName == 'Regularization':
        #regularizationDecisionId
        if idMap[modelName]:
            if idMap[modelName][added['regularizationDecisionId']]:
                added['regularizationDecisionId'] = idMap[modelName][added['regularizationDecisionId']]

    return generalPushUpdate(request, added, obj, addModel, savePoint)


def getForm(modelName):
    
    if modelName == 'Permissions':
        return AddPermissions
    elif modelName == 'Demonstrator':
        return AddDemonstrator
    elif modelName == 'UniversityDegree':
        return AddUniversityDegree
    elif modelName == 'Nomination':
        return AddNomination
    elif modelName == 'AdjectiveChange':
        return AddAdjectiveChange
    elif modelName == 'CertificateOfExcellence':
        return AddCertificateOfExcellence
    elif modelName == 'GraduateStudies':
        return AddGraduateStudies
    elif modelName == 'Dispatch':
        return AddDispatch
    elif modelName == 'Report':
        return AddReport
    elif modelName == 'Regularization':
        return AddRegularization
    elif modelName == 'Extension':
        return AddExtension
    elif modelName == 'Freeze':
        return AddFreeze
    elif modelName == 'DurationChange':
        return AddDurationChange
    elif modelName == 'AlimonyChange':
        return AddAlimonyChange
    elif modelName == 'UniversityChange':
        return AddUniversityChange
    elif modelName == 'SpecializationChange':
        return AddSpecializationChange


@login_required(login_url='app:login')
def pushData(request):
    # make it post request
    if True:
        if request.user.is_superuser:
             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    data = None
                    idMap = {}
                    with open('uploads/synchronization.json', 'r') as f:
                        data = load(f)
                    
                    #delete offline changes before merge
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'UploadedFile']:
                            delObjs= model.objects.filter(isOffline=True).delete()

      
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            # add
                            for added in data[model.__name__]['added']:
                                isExist = model.objects.filter(pk=added['id'])
                                if isExist.count()>0:
                                    continue
                                id = generalPushAdd(request, added , addModel, model.__name__, idMap, savePoint)
                                if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                                if model.__name__ in ['Dispatch', 'Freeze', 'Extension', 'DurationChange']:
                                    dispatchId = 1
                                    if model.__name__ in ['Freeze', 'Extension', 'DurationChange']:
                                        dispatchId = added.dispatchDecisionId
                                    else:
                                        dispatchId = added.id
                                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                    dispatch = loads(dumps(dispatchSerialized.data))
                                    endDate = CalculateDispatchEndDate(dispatch)
                                    for dispatchItem in dispatchObject:
                                        dispatchItem.dispatchEndDate = endDate
                                        Dispatch.full_clean(self=dispatchItem)
                                        Dispatch.save(self=dispatchItem)
                                if model.__name__ == 'AdjectiveChange':
                                    demonId= added.studentId
                                    demonstrator = Demonstrator.objects.get(pk=demonId)
                                    demonstrator.currentAdjective = added.adjectiveChangeAdjective
                                    Demonstrator.full_clean(self=demonstrator)
                                    Demonstrator.save(self=demonstrator)
      
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            # update
                            for updated in data[model.__name__]['updated']:
                                objs= model.objects.filter(pk=updated['id'])
                                for obj in objs:
                                    id = generalUpdateHub(request, updated , obj, addModel, model.__name__, idMap, savePoint)
                                    if type(id) == ErrorDict: return render(request, 'registration/result.html', {'result': id})
                                    if model.__name__ in ['Dispatch', 'Freeze', 'Extension', 'DurationChange']:
                                        dispatchId = 1
                                        if model.__name__ in ['Freeze', 'Extension', 'DurationChange']:
                                            dispatchId = updated.dispatchDecisionId
                                        else:
                                            dispatchId = updated.id
                                        dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                        dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                        dispatch = loads(dumps(dispatchSerialized.data))
                                        endDate = CalculateDispatchEndDate(dispatch)
                                        for dispatchItem in dispatchObject:
                                            dispatchItem.dispatchEndDate = endDate
                                            Dispatch.full_clean(self=dispatchItem)
                                            Dispatch.save(self=dispatchItem)
                                    if model.__name__ == 'AdjectiveChange':
                                        demonId= updated.studentId
                                        demonstrator = Demonstrator.objects.get(pk=demonId)
                                        demonstrator.currentAdjective = updated.adjectiveChangeAdjective
                                        Demonstrator.full_clean(self=demonstrator)
                                        Demonstrator.save(self=demonstrator)
                 
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            # delete
                            for deleted in data[model.__name__]['deleted']:
                                if idMap[model.__name__]:
                                    if idMap[model.__name__][deleted.id]:
                                        deleted.id = idMap[model.__name__][deleted.id]
                                isExist = model.objects.filter(pk=deleted.id)
                                if isExist.count()==0:
                                    continue
                                deletedObj= model.objects.filter(pk=deleted.id).delete()
                                if model.__name__ in [ 'Freeze', 'Extension', 'DurationChange']:
                                    dispatchId = deletedObj.dispatchDecisionId
                                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                    dispatch = loads(dumps(dispatchSerialized.data))
                                    endDate = CalculateDispatchEndDate(dispatch)
                                    for dispatchItem in dispatchObject:
                                        dispatchItem.dispatchEndDate = endDate
                                        Dispatch.full_clean(self=dispatchItem)
                                        Dispatch.save(self=dispatchItem)
                                if model.__name__ == 'AdjectiveChange':
                                    demonId= deletedObj.studentId
                                    demonstrators= Demonstrator.objects.filter(pk=demonId)
                                    for demonstrator in demonstrators:
                                        demonstrator.currentAdjective = demonstrator['adjectiveChange'][len(demonstrator['adjectiveChange'])-1]
                                        Demonstrator.full_clean(self=demonstrator)
                                        Demonstrator.save(self=demonstrator)
                                deletedObject= DeletedObjects()
                                deletedObject.modelName= model.__name__
                                deletedObject.objectId = deleted.id
                                deletedObject.save()

                    temp = LastPull.objects.get(pk=1)
                    temp.waitingMerge = False
                    LastPull.save(self=temp)
                            
                    return render(request, 'registration/result.html', {'result': 'done'})
                except Exception as e:
                    print('error happend', str(e))
                    transaction.savepoint_rollback(savePoint)
                    return render(request, 'registration/result.html', {'result': 'done'}) 
        else:
            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/result.html', {'result': 'done'})


@login_required(login_url='app:login')
def GetAllUsers(request):
    users = User.objects.select_related().prefetch_related().all()
    print(users)
    return render(request, 'home/demonstrator.html', {'users': users})


def do_something(request):
        return render(request, "home/query.html")


@login_required(login_url='app:login')
def gett(request):
    data2 = ser.serialize('json', Demonstrator.objects.select_related().prefetch_related().all())
    
    return JsonResponse(data2, safe=False)

