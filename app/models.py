from django.db import models
from app.constantVariables import *
from django.contrib.auth.models import User
import datetime


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return self.filename


class UserSynchronization(models.Model):
    userId= models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'userSynchronization')
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class LastPull(models.Model):
    userId= models.OneToOneField(User,on_delete=models.CASCADE, related_name='lastPull')
    lastPullDate= models.DateTimeField(auto_now=True)
    waitingMerge= models.BooleanField(null=True, blank=True, default=False)


class Permissions(models.Model):
    userId= models.ManyToManyField(User, related_name='permissions', blank=True)
    permissionsCollege = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Demonstrator(models.Model):
    name = models.CharField(max_length=50)
    fatherName = models.CharField(max_length=50)
    motherName = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES)
    birthDate = models.DateField()
    home = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=25, validators=[
                              MOBILE_NUMBER_VALIDATOR])
    telephone = models.CharField(max_length=25, validators=[
                                 TELEPHONE_VALIDATOR], null=True, blank=True)
    maritalStatus = models.CharField(
        max_length=10, choices=MARITAL_CHOICES)
    militarySituation = models.CharField(
        max_length=25, choices=MILITARY_SITUATION_CHOICES)
    residence = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    currentAdjective = models.CharField(
        max_length=50, choices=ADJECTIVE_CHOICES,null=True, blank=True, default='demonstrator')
    nominationReason = models.CharField(
        max_length=25, choices=NOMINATION_REASON_CHOICES, null=True, blank=True)
    contestAnnouncementDate = models.DateField(null=True, blank=True)
    university = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    commencementAfterNominationDate = models.DateField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f'{self.name} {self.fatherName} son of {self.motherName  }'


class UniversityDegree(models.Model):
    universityDegree = models.OneToOneField(Demonstrator, on_delete=models.CASCADE,
                                            primary_key=True, related_name='universityDegree')
    universityDegreeUniversity = models.CharField(
        max_length=100)
    universityDegreeCollege = models.CharField(
        max_length=100)
    universityDegreeSection = models.CharField(
        max_length=100)
    universityDegreeYear = models.CharField(max_length=10, validators=[
        YEAR_VALIDATOR])
    universityDegreeAverage = models.DecimalField(
        max_digits=5, decimal_places=2)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Nomination(models.Model):
    nominationDecision = models.OneToOneField(
        Demonstrator, on_delete=models.CASCADE, primary_key=True, related_name='nominationDecision')
    nominationDecisionNumber = models.IntegerField()
    nominationDecisionDate = models.DateField()
    nominationDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class AdjectiveChange(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='adjectiveChange')
    adjectiveChangeDecisionNumber = models.IntegerField()
    adjectiveChangeDecisionDate = models.DateField()
    adjectiveChangeDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    adjectiveChangeAdjective = models.CharField(
        max_length=50, choices=ADJECTIVE_CHOICES)
    adjectiveChangeReason = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class CertificateOfExcellence(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='certificateOfExcellence')
    certificateOfExcellenceYear = models.CharField(
        max_length=1, choices=EXCELLENCE_YEAR_CHOICES)
    certificateOfExcellenceDegree = models.CharField(
        max_length=1, choices=EXCELLENCE_DEGREE_CHOICES)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class GraduateStudies(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='graduateStudies')
    graduateStudiesDegree = models.CharField(
        max_length=10, choices=GRADUATE_STUDIES_DEGREE_CHOICES)
    graduateStudiesUniversity = models.CharField(
        max_length=100)
    graduateStudiesCollege = models.CharField(
        max_length=100)
    graduateStudiesSection = models.CharField(
        max_length=100)
    graduateStudiesSpecialzaion = models.CharField(
        max_length=100)
    graduateStudiesYear = models.CharField(max_length=10, validators=[
        YEAR_VALIDATOR])
    graduateStudiesAverage = models.DecimalField(
        max_digits=5, decimal_places=2)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Dispatch(models.Model):
    studentId = models.ForeignKey(
        Demonstrator, on_delete=models.CASCADE, related_name='dispatch')
    dispatchDecisionNumber = models.IntegerField()
    dispatchDecisionDate = models.DateField()
    dispatchDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    requiredCertificate = models.CharField(
        max_length=10, choices=CERTIFICATE_TYPE)
    dispatchType = models.CharField(
        max_length=10, choices=DISPATCH_TYPE)
    alimony = models.CharField(
        max_length=25, choices=ALIMONY)
    dispatchCountry = models.CharField(max_length=100)
    dispatchUniversity = models.CharField(
        max_length=100)
    dispatchDurationYear = models.IntegerField()
    dispatchDurationMonth = models.IntegerField()
    dispatchDurationDay = models.IntegerField()
    languageCourseDurationYear = models.IntegerField(null=True, blank=True, default=0)
    languageCourseDurationMonth = models.IntegerField(null=True, blank=True, default=0)
    languageCourseDurationDay = models.IntegerField(null=True, blank=True, default=0)
    dispatchEndDate = models.DateField(null=True, blank=True)
    backDate = models.DateField(null=True, blank=True)
    innerSupervisor = models.CharField(max_length=50, null=True, blank=True)
    outerSupervisor = models.CharField(max_length=50, null=True, blank=True)
    defenseDate = models.DateField(null=True, blank=True)
    gettingCertificateDate = models.DateField(null=True, blank=True)
    commencementDate = models.DateField(null=True, blank=True)
    atDisposalOfUniversityDate = models.DateField(null=True, blank=True)
    dispatchNotes = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastReportDate = models.DateField(null=True, blank=True, default=None)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)

    @property
    def remainingTime(self):
        if (self.dispatchEndDate):
            td = self.dispatchEndDate - self.commencementDate
            return td.days
        else:
            return None


class Report(models.Model):
    dispatchDecisionId = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='report')
    report = models.TextField()
    reportDate = models.DateField()
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Regularization(models.Model):
    regularizationDecisionId = models.OneToOneField(
        Dispatch, on_delete=models.CASCADE, primary_key=True, related_name='regularization')
    regularizationDecisionNumber = models.IntegerField()
    regularizationDecisionDate = models.DateField()
    regularizationDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    regularizationDecisionNotes = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Extension(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='extension')
    extensionDecisionNumber = models.IntegerField()
    extensionDecisionDate = models.DateField()
    extensionDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    extensionDurationYear = models.IntegerField()
    extensionDurationMonth = models.IntegerField()
    extensionDurationDay = models.IntegerField()
    emailSent = models.BooleanField(null=True, blank=True, default=False)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class Freeze(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='freeze')
    freezeDecisionNumber = models.IntegerField()
    freezeDecisionDate = models.DateField()
    freezeDecisionType = models.CharField(
        max_length=10, choices=DECISION_TYPE_CHOICES)
    freezeDurationYear = models.IntegerField()
    freezeDurationMonth = models.IntegerField()
    freezeDurationDay = models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class DurationChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='durationChange')
    durationChangeDurationYear = models.IntegerField()
    durationChangeDurationMonth = models.IntegerField()
    durationChangeDurationDay = models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class AlimonyChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='alimonyChange')
    newAlimony = models.CharField(
        max_length=25, choices=ALIMONY)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class UniversityChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='universityChange')
    newUniversity = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class SpecializationChange(models.Model):
    dispatchDecisionId = models.ForeignKey(
        Dispatch, on_delete=models.CASCADE, related_name='specializationChange')
    newSpecialization = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    isOffline = models.BooleanField(null=True, blank=True, default=False)
    modifiedByOffline = models.BooleanField(null=True, blank=True, default=False)


class DeletedObjects(models.Model):
    modelName = models.CharField(max_length=255)
    objectId = models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=datetime.datetime.now)
    isOffline = models.BooleanField(null=True, blank=True, default=False)


