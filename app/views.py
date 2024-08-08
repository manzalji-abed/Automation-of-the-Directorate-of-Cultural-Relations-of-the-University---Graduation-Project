import datetime
import pythoncom
import time
import win32com.client
from django.shortcuts import render, redirect,get_object_or_404
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
from httplib2.error import ServerNotFoundError



import smtplib
import ssl
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

Late_Emails=[]

def ExtensionMessage(informationForEmail):
    typeName={
        's': 'ش.ع',
        'o': 'و',
        'b': 'ب'
    }
    message="المعيد "+informationForEmail['name']+" بن "+informationForEmail['fatherName']+"\n\n\n\n\n\n\n\
بناء على القرار رقم "+str(informationForEmail['extensionDecisionNumber'])+"/"+ typeName[informationForEmail['extensionDecisionType']]+" تاريخ "+str(informationForEmail['extensionDecisionDate'])+" تم تمديد عملك كمعيد لمدة "+str(informationForEmail['extensionDurationYear'])+"سنة و "+str(informationForEmail['extensionDurationMonth'])+" شهر و "+str(informationForEmail['extensionDurationDay'])+" يوم" 
    return message



@login_required(login_url='app:login')
def UploadFile(request):
    print('lmmm22')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if os.path.exists("uploads/synchronization.json"):
                os.remove("uploads/synchronization.json")
                print('lmmm')
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
def downloadDocumentation(request):
    response = FileResponse(open("docs/docs.pdf", 'rb'))
    response['Content-Disposition'] = 'attachment; filename=' + "docs.pdf"
    response['Content-Type'] = 'application/octet-stream'
    return response


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


def SendEmailHotmail(email,subject,message):
    ol=win32com.client.Dispatch("outlook.application",pythoncom.CoInitialize())
    olmailitem=0x0 
    newmail=ol.CreateItem(olmailitem)
    newmail.Subject= subject
    newmail.To=email
    newmail.CC=email
    newmail.Body=message
    newmail.Send()

def SendEmailAlbaath(email,subject,message):
    smtp_server = "hostname"
    port =port   
    sender_email = "sender email"
    receiver_email = email
    password = 'your password'
    msg = f"Subject: {subject}\n\n{message}".encode('utf-8').strip()

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)
        
    print("Email sent successfully!")



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
        message = MIMEText(message,'plain','utf-8')
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

    except Exception as error:
        # TODO(developer) - Handle errors from gmail API.
        return error

@login_required(login_url='app:login')
def SendEmails(request):
    if request.user.is_superuser:
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
                    print(college)
                    for x in range(len(college)):
                        if college[x]['email']:
                            if college[x]['email'] not in emails:
                                emails.append(college[x]['email'])
                    print(emails)



                

                emails_str=""

                for x in emails:
                    emails_str+=x+", "
                    if request.POST['server'] == 'gmail':
                        gm=SendEmailGmail(x,request.POST['subject'],request.POST['msg'])
                        print("dndkfn",type(gm))
                        if type(gm) == ServerNotFoundError:
                            raise Exception("error")
                    elif request.POST['server'] == 'hotmail':
                        SendEmailHotmail(x,request.POST['subject'],request.POST['msg'])
                    elif request.POST['server'] == 'albaath':
                        SendEmailAlbaath(x,request.POST['subject'],request.POST['msg'])

                emails_str=emails_str[:-2]
                return render(request, 'home/success.html', {"emails": emails})


            except Exception as error:
                # TODO(developer) - Handle errors from gmail API.
                print(error)
                messages.add_message(request, messages.ERROR,"تأكد من معلوماتك واتصالك بالانترنت")
                return render(request, 'home/send_email.html')


            

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
                    SendEmailGmail(x," إنذار بانتهاء المدة القانونية الخاصة بك",message)
                elif request.POST['server'] == 'hotmail':
                    SendEmailHotmail(x," إنذار بانتهاء المدة القانونية الخاصة بك",message)
                elif request.POST['server'] == 'albaath':
                    SendEmailAlbaath(x," إنذار بانتهاء المدة القانونية الخاصة بك",message)

            emails_str=emails_str[:-2]

            return render(request, 'home/success.html', {"emails": emails})
        elif request.POST['emails'] == 'unsent':
            emails=[]
            if request.user.is_superuser:
                information=ShowUnsentEmails(request)
                extensions= information['extensions']
                for extension in extensions:
                    college= list(Dispatch.objects.filter(pk=extension.dispatchDecisionId.id).values('studentId__college', 'studentId__name', 'studentId__fatherName','studentId__email','dispatchEndDate'))
                    informationForEmail={ 'name': college[0]['studentId__name'],
                                    'fatherName': college[0]['studentId__fatherName'],
                                    'email': college[0]['studentId__email'],
                                    'extensionDecisionNumber': extension.extensionDecisionNumber,
                                    'extensionDecisionDate': extension.extensionDecisionDate,
                                    'extensionDecisionType': extension.extensionDecisionType,
                                    'extensionDurationYear': extension.extensionDurationYear,
                                    'extensionDurationMonth': extension.extensionDurationMonth,
                                    'extensionDurationDay': extension.extensionDurationDay,
                                    }
                    emails.append(informationForEmail['email'])
                                
                    try:
                        status=SendEmailAlbaath(informationForEmail['email'],"تمديد مدة العمل كمعيد",ExtensionMessage(informationForEmail))
                        if type(status) == ServerNotFoundError:
                            raise Exception("error")
                        Extension.objects.filter(id=extension.id).update(emailSent=True)
                    except Exception as error:
                        print(error)
                        messages.add_message(request, messages.ERROR,"تأكد من معلوماتك واتصالك بالانترنت")
            else:
                messages.add_message(request, messages.WARNING,"ليست لديك صلاحية الدخول إلى هذه الصفحة")
                return render(request, 'home/send_email.html')
            return render(request, 'home/success.html', {"emails": emails})
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية إرسال الإيميلات")
            return render(request, 'home/send_email.html')


def Email(request):
    # permissions= ser.serialize('json', Permissions.objects.all(),fields=('permissionsCollege'))
    permissions=list(Permissions.objects.all().values('permissionsCollege'))
    d = JsonResponse({"data": permissions})
    strr = d.content.decode("utf-8")

    late=GetLateEmails(request)
    if late== False:
            messages.add_message(request, messages.ERROR,"ليست لديك الصلاحية لهذه العملية")
            return render(request, 'home/send_email.html')

    unsent=ShowUnsentEmails(request)
    print(unsent)
    return render(request, 'home/send_email.html',{"select": strr,"late":late,"unsent":unsent["listOfExtensions"]})

@login_required(login_url='app:login')
def ShowUnsentEmails(request):
    extensions= list(Extension.objects.filter(emailSent=False))
    listOfExtensions= [] 
    for extension in extensions:
        college= list(Dispatch.objects.filter(pk=extension.dispatchDecisionId.id).values('studentId__college', 'studentId__name', 'studentId__fatherName','studentId__email','dispatchEndDate'))
        informationForEmail={ 'name': college[0]['studentId__name'],
                        'fatherName': college[0]['studentId__fatherName'],
                        'email': college[0]['studentId__email'],
                        'extensionDecisionNumber': extension.extensionDecisionNumber,
                        'extensionDecisionDate': extension.extensionDecisionDate,
                        'extensionDecisionType': extension.extensionDecisionType,
                        'extensionDurationYear': extension.extensionDurationYear,
                        'extensionDurationMonth': extension.extensionDurationMonth,
                        'extensionDurationDay': extension.extensionDurationDay,
                        }
        listOfExtensions.append(informationForEmail)
    ExtensionsInformation={"listOfExtensions":listOfExtensions,"extensions":extensions}
    return ExtensionsInformation

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


def generalInsert(request, mainField, baseDic, model, addModel, savePoint):
    id = None
    for i in range(len(request.POST.getlist(mainField))):
        dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']}
        dic.update(baseDic)
        for field in model._meta.local_fields:
            if field.name in request.POST:
                dic[field.name] = request.POST.getlist(field.name)[i]
        form = addModel(dic)
        if form.is_valid():
            id = form.save()
        else:
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
                try:
                    demonId = generalInsert(request, 'name', {}, Demonstrator, AddDemonstrator, savePoint)
                    if type(demonId) == ErrorDict: 
                        raise Exception('error')

                    id = generalInsert(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')

                    id = generalInsert(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')

                    id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')

                    id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة المعيد")
                    return redirect('app:insert')
                
            messages.add_message(request, messages.SUCCESS,"تم تسجيل المعيد")
            return redirect('app:insert')
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:insert')
    else:
        permissions=list(Permissions.objects.all().values('permissionsCollege'))
        d = JsonResponse({"data": permissions})
        strr = d.content.decode("utf-8")
        print(strr)
        return render(request, 'home/insert.html', {'select': strr})


@login_required(login_url='app:login')
def GraduateStudiesDegreeInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    id = generalInsert(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
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
                try:
                    id = generalInsert(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
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
def AdjectiveChangeInsert(request, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    id = generalInsert(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                    
                    demonstrator = Demonstrator.objects.get(pk=demonId)
                    demonstrator.currentAdjective = request.POST['adjectiveChangeAdjective']
                    Demonstrator.full_clean(self=demonstrator)
                    Demonstrator.save(self=demonstrator)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة تغيير الصفة")
                    return redirect('app:home')

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
                try:
                    dispatchId = generalInsert(request, 'dispatchDecisionNumber', {'studentId': demonId }, Dispatch, AddDispatch, savePoint)
                    if type(dispatchId) == ErrorDict: 
                        raise Exception('error')

                    id = generalInsert(request, 'regularizationDecisionNumber', {'regularizationDecisionId': dispatchId}, Regularization, AddRegularization, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة الإيفاد")
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
                try:
                    reportId = generalInsert(request, 'report', {'dispatchDecisionId': dispatchId}, Report, AddReport, savePoint)
                    if type(reportId) == ErrorDict: 
                        raise Exception('error')
                
                    dispatchs= Dispatch.objects.filter(pk=dispatchId)
                    for dispatch in dispatchs:
                        dispatch.lastReportDate = request.POST['reportDate']
                        Dispatch.full_clean(self=dispatch)
                        Dispatch.save(self=dispatch)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة التقرير")
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
                try:
                    extensionId = generalInsert(request, 'extensionDecisionNumber', {'dispatchDecisionId': dispatchId}, Extension, AddExtension, savePoint)
                    if type(extensionId) == ErrorDict: 
                        raise Exception('error')
                    
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة التمديد")
                    return redirect('app:demonstrator', id= demonId)

            informationForEmail={ 'name': college[0]['studentId__name'],
                            'fatherName': college[0]['studentId__fatherName'],
                            'email': college[0]['studentId__email'],
                            'extensionDecisionNumber': request.POST['extensionDecisionNumber'],
                            'extensionDecisionDate': request.POST['extensionDecisionDate'],
                            'extensionDecisionType': request.POST['extensionDecisionType'],
                            'extensionDurationYear': request.POST['extensionDurationYear'],
                            'extensionDurationMonth': request.POST['extensionDurationMonth'],
                            'extensionDurationDay': request.POST['extensionDurationDay'],
                            }
            try:
                status=SendEmailGmail(informationForEmail['email'],"تمديد مدة العمل كمعيد",ExtensionMessage(informationForEmail))
                if type(status) == ServerNotFoundError:
                    raise Exception("error")
                # print(informationForEmail['email'])
                Extension.objects.filter(id=extensionId.id).update(emailSent=True)
                messages.add_message(request, messages.SUCCESS,"تم إضافة التمديد وتم إرسال الايميل للمعيد")
                return redirect('app:demonstrator', id= demonId)
            except Exception as error:
                Extension.objects.filter(id=extensionId.id).update(emailSent=False)
                messages.add_message(request, messages.WARNING," تم إضافة التمديد ولكن لم يتم إرسال الايميل بسبب خطأ في الاتصال")
                return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الإضافة في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)
    else:
        return render(request, 'home/ext.html')


@login_required(login_url='app:login')
def SendExtensionEmail(request, dispatchId, demonId, extensionId):
    if request.method == 'GET':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college', 'studentId__name', 'studentId__fatherName','studentId__email','dispatchEndDate'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                
                obj = get_object_or_404(Extension, pk=extensionId)
                informationForEmail={ 'name': college[0]['studentId__name'],
                                'fatherName': college[0]['studentId__fatherName'],
                                'email': college[0]['studentId__email'],
                                'extensionDecisionNumber': obj.extensionDecisionNumber,
                                'extensionDecisionDate': obj.extensionDecisionDate,
                                'extensionDecisionType': obj.extensionDecisionType,
                                'extensionDurationYear': obj.extensionDurationYear,
                                'extensionDurationMonth': obj.extensionDurationMonth,
                                'extensionDurationDay': obj.extensionDurationDay,
                                }
                try:
                    status=SendEmailGmail(informationForEmail['email'],"هيلوز","بيباي")
                    if type(status) == ServerNotFoundError:
                        raise Exception("error")
                    # print(informationForEmail['email'])
                    Extension.objects.filter(id=extensionId).update(emailSent=True)
                    messages.add_message(request, messages.SUCCESS,"تم إرسال الايميل للمعيد")
                    return redirect('app:demonstrator', id= demonId)
                except Exception as error:
                    Extension.objects.filter(id=extensionId).update(emailSent=False)
                    messages.add_message(request, messages.WARNING,"لم يتم إرسال الايميل بسبب خطأ في الاتصال")
                    return redirect('app:demonstrator', id= demonId)
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية التعديل في هذه الكلية")
            return redirect('app:demonstrator', id= demonId)
    


@login_required(login_url='app:login')
def FreezeInsert(request, dispatchId,demonId):
    if request.method == 'POST':
        college= list(Dispatch.objects.filter(pk=dispatchId).values('studentId__college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['studentId__college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    freezeId = generalInsert(request, 'freezeDecisionNumber', {'dispatchDecisionId': dispatchId}, Freeze, AddFreeze, savePoint)
                    if type(freezeId) == ErrorDict: 
                        raise Exception('error')

                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة التجميد")
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
                try:
                    id = generalInsert(request, 'durationChangeDurationYear', {'dispatchDecisionId': dispatchId}, DurationChange, AddDurationChange, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة تغيير المدة")
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
                try:
                    id = generalInsert(request, 'newAlimony', {'dispatchDecisionId': dispatchId}, AlimonyChange, AddAlimonyChange, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة تغيير النفقة")
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
                try:
                    id = generalInsert(request, 'newUniversity', {'dispatchDecisionId': dispatchId}, UniversityChange, AddUniversityChange, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة تغيير الجامعة")
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
                try:
                    id = generalInsert(request, 'newSpecialization', {'dispatchDecisionId': dispatchId}, SpecializationChange, AddSpecializationChange, savePoint)
                    if type(id) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة تغيير الاختصاص")
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
    demonstrator = get_object_or_404(Demonstrator.objects.select_related().prefetch_related().all(), pk=id)
    permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
    return render(request, 'home/demonstrator.html', {'demonstrator': demonstrator, 'permissions': permissionList})
   

@login_required(login_url='app:login')
def GetAllEmails(request):
    if request.method == 'POST':
        all = Demonstrator.objects.filter().values('email', 'mobile', 'name')
        return render(request, 'registration/result.html', {'result': 'done'})


def GetLateEmails(request):
    if request.user.is_superuser:
        if request.method == 'GET':
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
            
            Late_Emails = list(Demonstrator.objects.filter(pk__in=res).values('email','mobile', 'name'))
            return Late_Emails
    else:
            return False



@login_required(login_url='app:login')
def GetCollegeEmails(request):
    if request.method == 'POST':
        college = Demonstrator.objects.filter(college=request.POST['college']).values('email', 'mobile', 'name')
        return render(request, 'registration/result.html', {'result': 'done'})


def generalUpdate(request, mainField, baseDic, model, addModel, obj, savePoint):
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
            print(form.errors)
            return form.errors
    return id


@login_required(login_url='app:login')
def UpdateDemonstrator(request, id):
    if request.method == 'POST':
        get_object_or_404(Demonstrator, pk=id)
        college= list(Demonstrator.objects.filter(pk=id).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    demonstrators = Demonstrator.objects.filter(pk=id)
                    for demonstrator in demonstrators:
                        demonId= generalUpdate(request, 'name', {}, Demonstrator, AddDemonstrator, demonstrator, savePoint)
                        if type(demonId) == ErrorDict:
                            raise Exception('error')
                    
                    nominations= Nomination.objects.filter(nominationDecision_id=id)
                    for nomination in nominations:
                        print(nomination)
                        resId = generalUpdate(request, 'nominationDecisionNumber', {'nominationDecision': id}, Nomination, AddNomination, nomination, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateUniversityDegree(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(UniversityDegree, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityDegrees= UniversityDegree.objects.filter(pk=id)
                    for universityDegree in universityDegrees:
                        resId = generalUpdate(request, 'universityDegreeUniversity', {'universityDegree': demonId}, UniversityDegree, AddUniversityDegree, universityDegree, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateNomination(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    
                    nominations= Nomination.objects.filter(pk=id)
                    for nomination in nominations:
                        resId = generalUpdate(request, 'nominationDecisionNumber', {'nominationDecision': demonId}, Nomination, AddNomination, nomination, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateAdjectiveChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    adjectiveChange= AdjectiveChange.objects.filter(pk=id)
                    for model in adjectiveChange:
                        resId = generalUpdate(request, 'adjectiveChangeDecisionNumber', {'studentId': demonId}, AdjectiveChange, AddAdjectiveChange, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')

                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrators= Demonstrator.objects.filter(pk=demonId)
                        for demonstrator in demonstrators:
                            demonstrator.currentAdjective = demonstrator['adjectiveChange'][len(demonstrator['adjectiveChange'])-1]
                            Demonstrator.full_clean(self=demonstrator)
                            Demonstrator.save(self=demonstrator)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateCertificateOfExcellence(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    certificateOfExcellence= CertificateOfExcellence.objects.filter(pk=id)
                    for model in certificateOfExcellence:
                        resId = generalUpdate(request, 'certificateOfExcellenceYear', {'studentId': demonId}, CertificateOfExcellence, AddCertificateOfExcellence, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateGraduateStudies(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(GraduateStudies, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    graduateStudies= GraduateStudies.objects.filter(pk=id)
                    for model in graduateStudies:
                        resId = generalUpdate(request, 'graduateStudiesDegree', {'studentId': demonId}, GraduateStudies, AddGraduateStudies, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateDispatch(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Dispatch, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    dispatchs= Dispatch.objects.filter(pk=id)
                    for dispatch in dispatchs:
                        dispatchId = generalUpdate(request, 'dispatchDecisionNumber', {'studentId': demonId}, Dispatch, AddDispatch, dispatch, savePoint)
                        if type(dispatchId) == ErrorDict:
                            raise Exception('error')

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=id)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})
                
            return JsonResponse({"status": "good" , 'endDate': endDate})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateReport(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    reports= Report.objects.filter(pk=id)
                    for report in reports:
                        resId = generalUpdate(request, 'regularizationDecisionNumber', {'dispatchDecisionId': report.dispatchDecisionId}, Report, AddReport, report, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateRegularization(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    regularizations= Regularization.objects.filter(pk=id)
                    for regularization in regularizations:
                        resId = generalUpdate(request, 'regularizationDecisionNumber', {'regularizationDecisionId': regularization.regularizationDecisionId}, Regularization, AddRegularization, regularization, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateExtension(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Extension, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    extensions= Extension.objects.filter(pk=id)
                    dispatchId = -1
                    for extension in extensions:
                        dispatchId= extension.dispatchDecisionId.id
                        extensionId = generalUpdate(request, 'extensionDecisionNumber', {'dispatchDecisionId': extension.dispatchDecisionId}, Extension, AddExtension, extension, savePoint)
                        if type(extensionId) == ErrorDict:
                            raise Exception('error')

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    print(str(e))
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateFreeze(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Freeze, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    freezes= Freeze.objects.filter(pk=id)
                    dispatchId=-1
                    for freeze in freezes:
                        dispatchId= freeze.dispatchDecisionId.id
                        freezeId = generalUpdate(request, 'freezeDecisionNumber', {'dispatchDecisionId': freeze.dispatchDecisionId}, Freeze, AddFreeze, freeze, savePoint)
                        if type(freezeId) == ErrorDict:
                            raise Exception('error')

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    print(str(e))
                    transaction.savepoint_rollback(savePoint)
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateDurationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    durationChange= DurationChange.objects.filter(pk=id)
                    dispatchId=-1
                    for model in durationChange:
                        dispatchId=model.dispatchDecisionId
                        resId = generalUpdate(request, 'durationChangeDurationYear', {'dispatchDecisionId': model.dispatchDecisionId}, DurationChange, AddDurationChange, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateAlimonyChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    alimonyChange= AlimonyChange.objects.filter(pk=id)
                    for model in alimonyChange:
                        resId = generalUpdate(request, 'newAlimony', {'dispatchDecisionId': model.dispatchDecisionId}, AlimonyChange, AddAlimonyChange, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateUniversityChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityChange= UniversityChange.objects.filter(pk=id)
                    for model in universityChange:
                        resId = generalUpdate(request, 'newUniversity', {'dispatchDecisionId': model.dispatchDecisionId}, UniversityChange, AddUniversityChange, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def UpdateSpecializationChange(request, id, demonId):
    if request.method == 'POST':
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    specializationChange= SpecializationChange.objects.filter(pk=id)
                    for model in specializationChange:
                        resId = generalUpdate(request, 'newSpecialization', {'dispatchDecisionId': model.dispatchDecisionId}, SpecializationChange, AddSpecializationChange, model, savePoint)
                        if type(resId) == ErrorDict:
                            raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})
 
def generalDelete(modelName, objectId):
    deletedObject= DeletedObjects()
    deletedObject.modelName= modelName
    deletedObject.objectId = objectId
    deletedObject.save()


@login_required(login_url='app:login')
def DeleteDemonstrator(request, id):
    if request.method == 'POST':
        get_object_or_404(Demonstrator, pk=id)
        college= list(Demonstrator.objects.filter(pk=id).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college'] in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    demonstrators = Demonstrator.objects.filter(pk=id).delete()
                    generalDelete('Demonstrator', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteUniversityDegree(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(UniversityDegree, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityDegrees= UniversityDegree.objects.filter(pk=id).delete()
                    generalDelete('UniversityDegree', id)  
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteNomination(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Nomination, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    nominations= Nomination.objects.filter(pk=id).delete()
                    generalDelete('Nomination', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteAdjectiveChange(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(AdjectiveChange, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    adjectiveChange= AdjectiveChange.objects.filter(pk=id).delete()
                    generalDelete('AdjectiveChange', id)
                
                    if 'adjectiveChangeAdjective' in request.POST:
                        demonstrators= Demonstrator.objects.filter(pk=demonId)
                        for demonstrator in demonstrators:
                            demonstrator.currentAdjective = demonstrator['adjectiveChange'][len(demonstrator['adjectiveChange'])-1]
                            Demonstrator.full_clean(self=demonstrator)
                            Demonstrator.save(self=demonstrator)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteCertificateOfExcellence(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(CertificateOfExcellence, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    certificateOfExcellence= CertificateOfExcellence.objects.filter(pk=id).delete()
                    generalDelete('CertificateOfExcellence', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteGraduateStudies(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(GraduateStudies, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    graduateStudies= GraduateStudies.objects.filter(pk=id).delete()
                    generalDelete('GraduateStudies', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})


            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteDispatch(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Dispatch, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    dispatchs= Dispatch.objects.filter(pk=id).delete()
                    generalDelete('Dispatch', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})
                

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteReport(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Report, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    reports= Report.objects.filter(pk=id).delete()
                    generalDelete('Report', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteRegularization(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Regularization, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    regularizations= Regularization.objects.filter(pk=id).delete()
                    generalDelete('Regularization', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteExtension(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Extension, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    extensions2= Extension.objects.filter(pk=id)
                    dispatchId = -1
                    for extension in extensions2:
                        dispatchId= extension.dispatchDecisionId.id
                    extensions= Extension.objects.filter(pk=id).delete()
                    generalDelete('Extension', id)

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteFreeze(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(Freeze, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    freezes2= Freeze.objects.filter(pk=id)
                    dispatchId=-1
                    for freeze in freezes2:
                        dispatchId= freeze.dispatchDecisionId.id

                    freezes= Freeze.objects.filter(pk=id).delete()
                    generalDelete('Freeze', id)

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good", 'endDate': endDate})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteDurationChange(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(DurationChange, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    durationChange2= DurationChange.objects.filter(pk=id)
                    dispatchId=-1
                    for model in durationChange2:
                        dispatchId=model.dispatchDecisionId.id

                    durationChange= DurationChange.objects.filter(pk=id).delete()
                    generalDelete('DurationChange', id)

                    endDate = ""
                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                    dispatch = loads(dumps(dispatchSerialized.data))
                    if dispatch[0]['commencementDate']:
                        endDate = CalculateDispatchEndDate(dispatch)
                        for dispatchItem in dispatchObject:
                            dispatchItem.dispatchEndDate = endDate
                            Dispatch.full_clean(self=dispatchItem)
                            Dispatch.save(self=dispatchItem)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteAlimonyChange(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(AlimonyChange, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    alimonyChange= AlimonyChange.objects.filter(pk=id).delete()
                    generalDelete('AlimonyChange', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteUniversityChange(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(UniversityChange, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    universityChange= UniversityChange.objects.filter(pk=id).delete()
                    generalDelete('UniversityChange', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def DeleteSpecializationChange(request, id, demonId):
    if request.method == 'POST':
        get_object_or_404(SpecializationChange, pk=id)
        college= list(Demonstrator.objects.filter(pk=demonId).values('college'))
        permissionList= [perm.permissionsCollege for perm in request.user.permissions.all()]
        if college[0]['college']  in permissionList or request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    specializationChange= SpecializationChange.objects.filter(pk=id).delete()
                    generalDelete('SpecializationChange', id)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return JsonResponse({"status": "bad"})

            return JsonResponse({"status": "good"})
        else :
            return JsonResponse({"status": "bad", "message": 'ليست لديك الصلاحية للقيام بهذه العملية'})


@login_required(login_url='app:login')
def QueryDemonstrator(request):
    if request.method == 'POST':        
        
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
                        else: obj = obj & Q(**{q+p: item[q][p]})
                else: 
                    if op == 'or':
                        obj = obj | Q(**{q: item[q]})
                    else: 
                        obj = obj & Q(**{q: item[q]})
            return obj
        
        query = loads(request.POST['query'])
        op = list(query.keys())[0]
        obj = makeQuery(query[op], op)
        result= Demonstrator.objects.filter(obj)
        da = SerializerDemonstrator(result, many=True)
        finalResult={}
        if len(da.data):
            finalResult= loads(dumps(da.data))
        dat = JsonResponse({"data": finalResult})
        stringgg = dat.content.decode('utf-8')
        return render(request, "registration/result.html", {"result":stringgg, 'fields': request.POST['cols']})


@login_required(login_url='app:login')
def home(request):
    result={}
    result['allDemons'] = Demonstrator.objects.filter().distinct().count()
    todayDate= datetime.date.today() 
    result['allInDispatch'] = Demonstrator.objects.filter(Q(**{'dispatch__dispatchEndDate__gte': todayDate})).distinct().count()
    result['master'] = Demonstrator.objects.filter(Q(**{'dispatch__dispatchEndDate__gte': todayDate}) & Q(**{'dispatch__requiredCertificate':'master'})).distinct().count()
    result['ph.d'] = Demonstrator.objects.filter(Q(**{'dispatch__dispatchEndDate__gte': todayDate}) & Q(**{'dispatch__requiredCertificate':'ph.d'})).distinct().count()
    result['others'] = result['allDemons'] - result['master'] - result['ph.d']
    for adjective in ADJECTIVE_CHOICES:
        result[adjective[0]] = Demonstrator.objects.filter(currentAdjective= adjective[0]).distinct().count()
    result['phd'] = result['ph.d']
    result['returning_demonstrator'] = result['returning demonstrator']
    result['transfer_outside_the_university'] = result['transfer outside the university']
    result['end_services'] = result['end services']
    return render(request, 'home/home.html', {'statistics': result}) 


def Test(request):
    LastPull.objects.create(userId= request.user, lastPullDate=datetime.datetime.now)
    UserSynchronization.objects.create(userId= request.user)



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
    elif modelName == 'UserSynchronization':
        return SerializerUserSynchronization


@login_required(login_url='app:login')
def pullData(request):
    if request.method=='POST':
        if request.user.is_superuser:
             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    if 'lastPull' in request.POST and request.POST['lastPull'] == '1':
                        lastPullDate= request.user.lastPull.lastPullDate
                    elif 'pullDate' in request.POST:
                        lastPullDate= datetime.datetime.strptime(request.POST['pullDate'], '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
                    else:
                        lastPullDate= request.user.lastPull.lastPullDate

                        
                    data={}
                    for model in apps.get_models():
                        if model.__name__ == 'UserSynchronization':
                            serializerClass = getSerializer(model.__name__)
                            added = serializerClass(model.objects.filter(createdDate__gte=lastPullDate), many= True).data
                            updated =serializerClass(model.objects.filter(Q(lastModifiedDate__gte=lastPullDate) & ~Q(createdDate__gte=lastPullDate) ), many= True).data
                            deleted = SerializerDeletedObjects( DeletedObjects.objects.filter(modelName=model.__name__, createdDate__gte=lastPullDate), many= True).data
                            added2 = SerializerUser(User.objects.filter(userSynchronization__createdDate__gte=lastPullDate), many= True).data
                            updated2 =SerializerUser(User.objects.filter(Q(userSynchronization__lastModifiedDate__gte=lastPullDate) & ~Q(userSynchronization__createdDate__gte=lastPullDate) ), many= True).data
                            deleted2 = SerializerDeletedObjects( DeletedObjects.objects.filter(modelName='User', createdDate__gte=lastPullDate), many= True).data
                            data.update( {'User': {'updated':updated2, 'added':added2, 'deleted': deleted2} })
                            data.update( {model.__name__: {'updated':updated, 'added':added, 'deleted': deleted} })
                        elif not model.__name__ in ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            serializerClass = getSerializer(model.__name__)
                            added = serializerClass(model.objects.filter(createdDate__gte=lastPullDate), many= True).data
                            updated =serializerClass(model.objects.filter(Q(lastModifiedDate__gte=lastPullDate) & ~Q(createdDate__gte=lastPullDate) ), many= True).data
                            deleted = SerializerDeletedObjects( DeletedObjects.objects.filter(modelName=model.__name__, createdDate__gte=lastPullDate), many= True).data
                            data.update( {model.__name__: {'updated':updated, 'added':added, 'deleted': deleted} })
                    with open('uploads/synchronization.json', 'w') as file:
                        dump(data, file, indent=None)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    return render(request, 'registration/result.html', {'result': 'done'}) 
                
             temp = LastPull.objects.get(userId_id__id=request.user.id)
             temp.lastPullDate=datetime.datetime.now
             LastPull.save(self=temp)

             response = FileResponse(open("uploads/synchronization.json", 'rb'))
             response['Content-Disposition'] = 'attachment; filename=' + "synchronization.json"
             response['Content-Type'] = 'application/octet-stream'
             return response

        else:
            return render(request, 'registration/result.html', {'result': 'done'})
    else:
        return render(request, 'registration/result.html', {'result': 'done'})


def generalPushAdd(request ,added, addModel, modelName, idMap, savePoint):
    id = None
    haveId = 'id' in added
    oldId= None
    if haveId:
        oldId = added['id']
        del added['id']
    dic = {'csrfmiddlewaretoken': get_token(request)}
    dic.update(added)
    if modelName != 'User':
        dic.update({'isOffline': False})
    form = addModel(dic)
    if form.is_valid():
        id = form.save()
        if haveId:
            if not modelName in idMap:
                idMap[modelName] = {}
            idMap[modelName].update({oldId: id.id})
        
    else:
        transaction.savepoint_rollback(savePoint)
        return form.errors
    return id 


def generalPushAddHub(request, added, addModel, modelName, idMap, savePoint):
    #Demonstrator
    if modelName in ['Dispatch', 'GraduateStudies', 'CertificateOfExcellence', 'AdjectiveChange']:
        #studentId
        if 'Demonstrator' in idMap:
            if added['studentId'] in idMap['Demonstrator']:
                added['studentId'] = idMap['Demonstrator'][added['studentId']]
    elif modelName == 'Nomination':
        #nominationDecision
        if 'Demonstrator' in idMap:
            if added['nominationDecision'] in idMap['Demonstrator']:
                added['nominationDecision'] = idMap['Demonstrator'][added['nominationDecision']]
    elif modelName == 'UniversityDegree':
        #universityDegree
        if 'Demonstrator' in idMap:
            if added['universityDegree'] in idMap['Demonstrator']:
                added['universityDegree'] = idMap['Demonstrator'][added['universityDegree']]

    #Dispatch
    elif modelName in ['Report', 'Extension', 'Freeze', 'DurationChange', 'AlimonyChange', 'UniversityChange', 'SpecializationChange']:
        #dispatchDecisionId
        if 'Dispatch' in idMap:
            if added['dispatchDecisionId'] in idMap['Dispatch']:
                added['dispatchDecisionId'] = idMap['Dispatch'][added['dispatchDecisionId']]
    elif modelName == 'Regularization':
        #regularizationDecisionId
        if 'Dispatch' in idMap:
            if added['regularizationDecisionId'] in idMap['Dispatch']:
                added['regularizationDecisionId'] = idMap['Dispatch'][added['regularizationDecisionId']]

    #User
    elif modelName in ['UserSynchronization', 'Permissions']:
        if 'User' in idMap:
            if modelName == 'UserSynchronization':
                if added['userId'] in idMap['User']:
                    added['userId'] = idMap['User'][added['userId']]
            else:
                userIdList=[]
                for userIdItem in added['userId']:
                    if userIdItem in idMap['User']:
                        userIdList.append(idMap['User'][userIdItem])
                    else:
                        userIdList.append(userIdItem)
                added['userId'] = userIdList
        
    
    return generalPushAdd(request, added , addModel, modelName, idMap, savePoint)


def generalPushUpdate(request, modelName, added, obj, addModel, savePoint):
    id = None
    dic = {'csrfmiddlewaretoken': get_token(request)}
    dic.update(added)
    if modelName != 'User':
        dic.update({'isOffline': False})
        dic.update({'modifiedByOffline': False})
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
        if modelName in idMap:
            if added['studentId'] in idMap[modelName]:
                added['studentId'] = idMap[modelName][added['studentId']]
    elif modelName == 'Nomination':
        #nominationDecision
        if modelName in idMap:
            if added['nominationDecision'] in idMap[modelName]:
                added['nominationDecision'] = idMap[modelName][added['nominationDecision']]
    elif modelName == 'UniversityDegree':
        #universityDegree
        if modelName in idMap:
            if added['universityDegree'] in idMap[modelName]:
                added['universityDegree'] = idMap[modelName][added['universityDegree']]

    #Dispatch
    elif modelName in ['Report', 'Extension', 'Freeze', 'DurationChange', 'AlimonyChange', 'UniversityChange', 'SpecializationChange']:
        #dispatchDecisionId
        if modelName in idMap:
            if added['dispatchDecisionId'] in idMap[modelName]:
                added['dispatchDecisionId'] = idMap[modelName][added['dispatchDecisionId']]
    elif modelName == 'Regularization':
        #regularizationDecisionId
        if modelName in idMap:
            if added['regularizationDecisionId'] in idMap[modelName]:
                added['regularizationDecisionId'] = idMap[modelName][added['regularizationDecisionId']]
    
    #User
    elif modelName in ['UserSynchronization', 'Permissions']:
        if 'User' in idMap:
            if modelName == 'UserSynchronization':
                if added['userId'] in idMap['User']:
                    added['userId'] = idMap['User'][added['userId']]
            else:
                userIdList=[]
                for userIdItem in added['userId']:
                    if userIdItem in idMap['User']:
                        userIdList.append(idMap['User'][userIdItem])
                    else:
                        userIdList.append(userIdItem)
                added['userId'] = userIdList

    return generalPushUpdate(request, modelName, added, obj, addModel, savePoint)


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
    elif modelName == 'User':
        return AddUser
    elif modelName == 'UserSynchronization':
        return AddUserSynchronization


@login_required(login_url='app:login')
def pushData(request):
    if request.method == 'POST':
        if request.user.is_superuser:
             form = UploadFileForm(request.POST, request.FILES)
             if form.is_valid():
                 if os.path.exists("uploads/synchronization.json"):
                     os.remove("uploads/synchronization.json")
                 # If a custom filename is provided, use it. Otherwise, use the original filename.
                 custom_filename = form.cleaned_data.get('custom_filename') or "synchronization"
                 # Create a new UploadedFile object and save it to the database
                 uploaded=request.FILES['file']
                 uploaded._name="synchronization.json"
                 uploaded_file = UploadedFile(file=uploaded, filename=custom_filename)
                 uploaded_file.save()

             with transaction.atomic():
                savePoint= transaction.savepoint()
                try:
                    data = None
                    idMap = {}
                    usersIds = []
                    unsentEmails=[]
                    with open('uploads/synchronization.json', 'r') as f:
                        data = load(f)

                    #add
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            for added in data[model.__name__]['added']:
                                if model.__name__ == 'User':
                                    usersIds.append(added['id'])
                                id = generalPushAddHub(request, added , addModel, model.__name__, idMap, savePoint)
                                if type(id) == ErrorDict:
                                    raise Exception(id)
                                if model.__name__ in ['Dispatch', 'Freeze', 'Extension', 'DurationChange']:
                                    dispatchId = 1
                                    if model.__name__ in ['Freeze', 'Extension', 'DurationChange']:
                                        dispatchId = added['dispatchDecisionId']
                                    else:
                                        dispatchId = id.id
                                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                    dispatch = loads(dumps(dispatchSerialized.data))
                                    if dispatch[0]['commencementDate']:
                                        endDate = CalculateDispatchEndDate(dispatch)
                                        for dispatchItem in dispatchObject:
                                            dispatchItem.dispatchEndDate = endDate
                                            Dispatch.full_clean(self=dispatchItem)
                                            Dispatch.save(self=dispatchItem)
                                if model.__name__ == 'AdjectiveChange':
                                    demonId= added.studentId
                                    demonstrator = Demonstrator.objects.get(pk=demonId)
                                    demonstrator.currentAdjective = added['adjectiveChangeAdjective']
                                    Demonstrator.full_clean(self=demonstrator)
                                    Demonstrator.save(self=demonstrator)
                                if model.__name__ == 'Extension' and not id.emailSent:
                                    college= list(Dispatch.objects.filter(pk=id.dispatchDecisionId.id).values('studentId__college', 'studentId__name', 'studentId__fatherName','studentId__email','dispatchEndDate'))
                                    informationForEmail={ 'name': college[0]['studentId__name'],
                                                    'fatherName': college[0]['studentId__fatherName'],
                                                    'email': college[0]['studentId__email'],
                                                    'extensionDecisionNumber': id.extensionDecisionNumber,
                                                    'extensionDecisionDate': id.extensionDecisionDate,
                                                    'extensionDecisionType': id.extensionDecisionType,
                                                    'extensionDurationYear': id.extensionDurationYear,
                                                    'extensionDurationMonth': id.extensionDurationMonth,
                                                    'extensionDurationDay': id.extensionDurationDay,
                                                    }
                                    try:
                                        status=SendEmailGmail(informationForEmail['email'],"هيلوز","بيباي")
                                        if type(status) == ServerNotFoundError:
                                            raise Exception("error")
                                        # print(informationForEmail['email'])
                                        Extension.objects.filter(id=id.id).update(emailSent=True)
                                    except Exception as error:
                                        unsentEmails.append('التمديد الخاص بالطالب '+college[0]['studentId__name']+' رقم '+str(id.extensionDecisionNumber)+' تاريخ '+str(id.extensionDecisionDate))

                    #update
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            for updated in data[model.__name__]['updated']:
                                idName = 'id'
                                if model.__name__ == 'UniversityDegree': idName = 'universityDegree'
                                elif model.__name__ == 'Nomination': idName = 'nominationDecision'
                                elif model.__name__ == 'Regularization': idName = 'regularizationDecisionId'

                                objs= model.objects.filter(pk=updated[idName])
                                for obj in objs:
                                    id = generalUpdateHub(request, updated , obj, addModel, model.__name__, idMap, savePoint)
                                    if type(id) == ErrorDict:
                                        raise Exception(id)
                                    if model.__name__ in ['Dispatch', 'Freeze', 'Extension', 'DurationChange']:
                                        dispatchId = 1
                                        if model.__name__ in ['Freeze', 'Extension', 'DurationChange']:
                                            dispatchId = updated['dispatchDecisionId']
                                        else:
                                            dispatchId = updated['id']
                                        dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                        dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                        dispatch = loads(dumps(dispatchSerialized.data))
                                        if dispatch[0]['commencementDate']:
                                            endDate = CalculateDispatchEndDate(dispatch)
                                            for dispatchItem in dispatchObject:
                                                dispatchItem.dispatchEndDate = endDate
                                                Dispatch.full_clean(self=dispatchItem)
                                                Dispatch.save(self=dispatchItem)
                                    if model.__name__ == 'AdjectiveChange':
                                        demonId= updated.studentId
                                        demonstrator = Demonstrator.objects.get(pk=demonId)
                                        demonstrator.currentAdjective = updated['adjectiveChangeAdjective']
                                        Demonstrator.full_clean(self=demonstrator)
                                        Demonstrator.save(self=demonstrator)

                    #delete             
                    for model in apps.get_models():
                        if not model.__name__ in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'LastPull', 'DeletedObjects', 'UploadedFile']:
                            addModel= getForm(model.__name__)
                            for deleted in data[model.__name__]['deleted']:
                                if model.__name__ in idMap and idMap[model.__name__]:
                                    if deleted['objectId'] in idMap[model.__name__] and idMap[model.__name__][deleted['objectId']]:
                                        deleted['objectId'] = idMap[model.__name__][deleted['objectId']]
                                deletedObj= model.objects.filter(pk=deleted['objectId']).delete()
                                if model.__name__ in [ 'Freeze', 'Extension', 'DurationChange']:
                                    dispatchId = deletedObj.dispatchDecisionId.id
                                    dispatchObject = Dispatch.objects.filter(pk=dispatchId)
                                    dispatchSerialized = SerializerDispatch(dispatchObject, many= True)
                                    dispatch = loads(dumps(dispatchSerialized.data))
                                    if dispatch[0]['commencementDate']:
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
                                deletedObject.objectId = deleted['objectId']
                                deletedObject.isOffline = False
                                deletedObject.save()

                    #add LastPull for added users
                    for userIdItem in usersIds:
                        haveLastPull = User.objects.filter(pk=userIdItem)
                        if 'lastPull' in haveLastPull:
                            continue
                        userId = userIdItem
                        if idMap['User']:
                            if idMap['User'][userId]:
                                userId = idMap['User'][userId]
                        LastPull.objects.create(userId= userId, lastPullDate=datetime.datetime.now)
                    
                    print(unsentEmails)
                    if len(unsentEmails) > 0:
                        messages.add_message(request, messages.SUCCESS,"تم تحديث المعلومات بنجاح , لم يتم إرسال بعض إيميلات التمديد بسبب خطأ في الاتصال")
                        return redirect('app:upload_file')
                    else:
                        messages.add_message(request, messages.SUCCESS,"تم تحديث المعلومات بنجاح")
                        return redirect('app:upload_file')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                    return redirect('app:upload_file')
        else:
            messages.add_message(request, messages.WARNING,"ليست لديك صلاحية الدخول إلى هذه الصفحة")
            return redirect('app:home')
    else:
        form = UploadFileForm()
        return render(request, 'home/upload.html', {'form': form})


@login_required(login_url='app:login')
def GetAllUsers(request):
    users = User.objects.select_related().prefetch_related().all()
    return render(request, 'home/demonstrator.html', {'users': users})


def do_something(request):
        return render(request, "home/query.html")


@login_required(login_url='app:login')
def gett(request):
    data2 = ser.serialize('json', Demonstrator.objects.select_related().prefetch_related().all())
    
    return JsonResponse(data2, safe=False)


@login_required(login_url='app:login')
def permissions_list(request):
    if request.user.is_superuser:
        query = request.GET.get('search')
        if query:
            permissions = Permissions.objects.filter(permissionsCollege__icontains=query)
        else:
            permissions = Permissions.objects.all()
        context = {'permissions': permissions, 'query': query}

        return render(request, 'home/permissions_list.html', context)
    else:
        messages.add_message(request, messages.ERROR,"لا تملك صلاحية  ")
        return redirect('app:home')


@login_required(login_url='app:login')
def permissions_detail(request, pk):
    if request.user.is_superuser:
        permissions = get_object_or_404(Permissions, pk=pk)
        if request.method == 'POST':
            users = request.POST.getlist('userId')
            permissions.userId.set(users)
            permissions.modifiedByOffline=False
            permissions.save()
        try:
            users = permissions.userId.all()
        except User.DoesNotExist:
            raise Http404("User does not exist")
        all_users = User.objects.all()
        context = {'permissions': permissions, 'users': users, 'all_users': all_users}
        return render(request, 'home/permissions_detail.html', context)
    else :
        messages.add_message(request, messages.ERROR,"لا تملك صلاحية  ")
        return redirect('app:home')


@login_required(login_url='app:login')
def PermissionInsert(request):
     if request.method == 'POST':
        if  request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    permissionId = generalInsert(request, 'permissionsCollege', {}, Permissions, AddPermissions, savePoint)
                    if type(permissionId) == ErrorDict: 
                        raise Exception('error')
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"عذرا حدث خطأ ما, لم تتم إضافة الكلية")
                    return redirect('app:permissions_list')
                
            messages.add_message(request, messages.SUCCESS,"تم تسجيل الكلية")
            return redirect('app:permissions_list')
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية إضافة الكلية")
            return redirect('app:permissions_list')


@login_required(login_url='app:login')
def DeletePermission(request, pk):
    if request.method == 'GET':
        if request.user.is_superuser:
            get_object_or_404(Permissions, pk=pk)
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    permissions = Permissions.objects.filter(pk=pk).delete()
                    generalDelete('Permissions', pk)
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                    return redirect('app:permissions_list')

            messages.add_message(request, messages.SUCCESS,"تم الحذف")
            return redirect('app:permissions_list')
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية حذف السماحية")
            return redirect('app:permissions_list')


@login_required(login_url='app:login')
def UpdatePermission(request, pk):
    if request.method == 'POST':
        if request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    permissions = get_object_or_404(Permissions, pk=pk)
                    demons = UniversityDegree.objects.filter(universityDegreeCollege=permissions.permissionsCollege)
                    demons.update(universityDegreeCollege=request.POST['permissionsCollege'])
                    permissions.permissionsCollege=(request.POST['permissionsCollege'])
                    permissions.modifiedByOffline=False
                    permissions.save()
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                    return redirect('app:permissions_detail', pk=pk)

            messages.add_message(request, messages.SUCCESS,"تم التعديل")
            return redirect('app:permissions_detail',pk=pk)
        else :
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية حذف السماحية")
            return redirect('app:permissions_detail',pk=pk)



@login_required(login_url='app:login')
def Register(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            checkPassword = authenticate(request, username=request.user.username, password=request.POST['admin_password'])
            if checkPassword is not None:
                with transaction.atomic():
                    savePoint = transaction.savepoint()
                    try:
                        dic = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                            'username':request.POST['username'],
                            'first_name':request.POST['firstName'],
                            'last_name':request.POST['lastName'],
                            'password':request.POST['password'],
                            'email':request.POST['email'],
                            'date_joined':datetime.datetime.now()
                            }
                        form = AddUser(dic)
                        if form.is_valid():
                            user = User.objects.create_user(
                            username=request.POST['username'],
                            first_name=request.POST['firstName'],
                            last_name=request.POST['lastName'],
                            password=request.POST['password'],
                            email=request.POST['email']
                            )
                        else:
                            raise Exception(form.errors)
                        for perm in request.POST.getlist('permissions'):
                            permission, created= Permissions.objects.get_or_create(permissionsCollege=perm)
                            user.permissions.add(permission.id)
                        LastPull.objects.create(userId= user, lastPullDate=datetime.datetime.now)
                        UserSynchronization.objects.create(userId= user)

                        messages.add_message(request, messages.SUCCESS,"تمت إضافة الموظف")
                        return redirect('app:register')
                    except Exception as e:
                        transaction.savepoint_rollback(savePoint)
                        print(e)
                        messages.add_message(request, messages.ERROR,'حدث خطأ ما')
                        return redirect('app:register')
            else:
                messages.add_message(request, messages.ERROR,"كلمة مرور المدير غير صحيحة")
                return redirect('app:register')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تسجيل موظفين")
            return redirect('app:register')

    if request.user.is_superuser:
        # permissions= ser.serialize('json', Permissions.objects.all(),fields=('permissionsCollege'))
        permissions=list(Permissions.objects.filter().values('permissionsCollege'))
        d = JsonResponse({"data": permissions})
        strr = d.content.decode("utf-8")
        
        return render(request, 'registration/register.html', {'colleges': strr })
    else:
        return render(request, 'registration/result.html', {'result': 'denied'})



@login_required(login_url='app:login')
def GetAllUsers(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    
                    return render(request, 'home/users.html', {'result': User.objects.filter().all()})
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                    return redirect('app:home')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الوصول إلى معلومات الموظفين")
            return redirect('app:home')


@login_required(login_url='app:login')
def GetUser(request, id):
    if request.method == 'POST':
        if request.user.is_superuser:
            with transaction.atomic():
                savePoint = transaction.savepoint()
                try:
                    user = get_object_or_404(User.objects.select_related().prefetch_related().all(), pk=id)
                    return render(request, 'home/home.html', {'result': user})
                except Exception as e:
                    transaction.savepoint_rollback(savePoint)
                    print(str(e))
                    messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                    return render(request, 'home/home.html')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية الوصول إلى معلومات الموظفين")
            return redirect('app:home')


@login_required(login_url='app:login')
def UpdateUser(request, id):
    if request.method == 'POST':
        if request.user.is_superuser:
            checkPassword = authenticate(request, username=request.user.username, password=request.POST['admin_password'])
            if checkPassword is not None:
                with transaction.atomic():
                    savePoint = transaction.savepoint()
                    try:
                        user = get_object_or_404(User, id=id)
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.email = request.POST['email']
                        user.username = request.POST['username']
                        user.save()
                        userSynchronization = UserSynchronization.objects.get(userId_id__id=id)
                        userSynchronization.modifiedByOffline=False
                        userSynchronization.save()
                    except Exception as e:
                        transaction.savepoint_rollback(savePoint)
                        print(str(e))
                        messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                        return redirect('app:user_list')
                messages.add_message(request, messages.SUCCESS,"تم التعديل بنجاح")
                return redirect('app:user_list')
            else:
                messages.add_message(request, messages.ERROR,"كلمة مرور المدير غير صحيحة")
                return redirect('app:user_list')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تعديل معلومات الموظفين")
            return redirect('app:user_list')


@login_required(login_url='app:login')
def UpdateUserPassword(request, id):
    if request.method == 'POST':
        if request.user.is_superuser:
            checkPassword = authenticate(request, username=request.user.username, password=request.POST['admin_password'])
            if checkPassword is not None:
                with transaction.atomic():
                    savePoint = transaction.savepoint()
                    try:
                        user = get_object_or_404(User, id=id)
                        user.set_password(request.POST['newPassword'])
                        user.save()
                        userSynchronization = UserSynchronization.objects.get(userId_id__id=id)
                        userSynchronization.modifiedByOffline=False
                        userSynchronization.save()
                    except Exception as e:
                        transaction.savepoint_rollback(savePoint)
                        print(str(e))
                        messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                        return redirect('app:user_list')
                messages.add_message(request, messages.SUCCESS,"تم تعديل كلمة المرور")
                return redirect('app:user_list')
            else:
                messages.add_message(request, messages.ERROR,"كلمة مرور المدير غير صحيحة")
                return redirect('app:user_list')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تعديل معلومات الموظفين")
            return redirect('app:user_list')


@login_required(login_url='app:login')
def MakeUserAdmin(request, id):
    if request.method == 'POST':
        if request.user.is_superuser:
            checkPassword = authenticate(request, username=request.user.username, password=request.POST['admin_password'])
            if checkPassword is not None:
                with transaction.atomic():
                    savePoint = transaction.savepoint()
                    try:
                        user = get_object_or_404(User, id=id)
                        user.is_superuser = True
                        user.save()
                        userSynchronization = UserSynchronization.objects.get(userId_id__id=id)
                        userSynchronization.modifiedByOffline=False
                        userSynchronization.save()
                    except Exception as e:
                        transaction.savepoint_rollback(savePoint)
                        print(str(e))
                        messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                        return redirect('app:user_list')
                messages.add_message(request, messages.SUCCESS,"تمت ترقية المستخدم")
                return redirect('app:user_list')
            else:
                messages.add_message(request, messages.ERROR,"كلمة مرور المدير غير صحيحة")
                return redirect('app:user_list')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تعديل معلومات الموظفين")
            return redirect('app:user_list')


@login_required(login_url='app:login')
def DeleteUser(request, id):
    if request.method == 'POST':
        if request.user.is_superuser:
            checkPassword = authenticate(request, username=request.user.username, password=request.POST['admin_password'])
            if checkPassword is not None:
                with transaction.atomic():
                    savePoint = transaction.savepoint()
                    try:
                        user = get_object_or_404(User, id=id)
                        user.delete()
                        generalDelete('User', id)
                    except Exception as e:
                        transaction.savepoint_rollback(savePoint)
                        print(str(e))
                        messages.add_message(request, messages.ERROR,"حدث خطأ ما")
                        return redirect('app:user_list')
                messages.add_message(request, messages.ERROR,"تم حذف المستخدم")
                return redirect('app:user_list')
            else:
                messages.add_message(request, messages.ERROR,"كلمة مرور المدير غير صحيحة")
                return redirect('app:user_list')
        else:
            messages.add_message(request, messages.ERROR,"لا تملك صلاحية تعديل معلومات الموظفين")
            return redirect('app:user_list')

def About(request):
    return render(request,"home/about-us.html")