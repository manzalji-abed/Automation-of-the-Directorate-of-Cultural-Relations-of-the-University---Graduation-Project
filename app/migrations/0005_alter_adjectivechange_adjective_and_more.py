# Generated by Django 4.1.4 on 2022-12-25 23:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_dispatchdecision_extension_nominaitiondecision_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjectivechange',
            name='adjective',
            field=models.CharField(blank=True, choices=[('demonstrator', 'معيد'), ('returning', 'عائد'), ('envoy', 'موفد'), ('returning demonstrator', 'معيد عائد'), ('loathes', 'مستنكف'), ('Transfer outside the university', 'نقل خارج الجامعة'), ('end services', 'انهاء خدمات'), ('resigned', 'انهاء بحكم المستقيل')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='adjectivechange',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adjectivechange',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adjectivechange',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='adjectivechange',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adjectivechange',
            name='studentId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adjectiveChange', to='app.demonstrator'),
        ),
        migrations.AlterField(
            model_name='alimonychange',
            name='dispatchDecisionNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alimonyChange', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='alimonychange',
            name='newAlimony',
            field=models.CharField(blank=True, choices=[('grant', 'منحة'), ('seat', 'مقعد')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='certificateofexcellence',
            name='degree',
            field=models.CharField(blank=True, choices=[('1', 'الأول'), ('2', 'الثاني'), ('3', 'الثالث')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='certificateofexcellence',
            name='studentId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificateOfExcellence', to='app.demonstrator'),
        ),
        migrations.AlterField(
            model_name='certificateofexcellence',
            name='year',
            field=models.CharField(blank=True, choices=[('1', 'سنة أولى'), ('2', 'سنة ثانية'), ('3', 'سنة ثالثة'), ('4', 'سنة رابعة'), ('5', 'سنة خامسة'), ('6', 'سنة سادسة'), ('g', 'تخرج')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='birthDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='commencementAfterNominationDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='contestAnnouncementDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='currentAdjective',
            field=models.CharField(blank=True, choices=[('demonstrator', 'معيد'), ('returning', 'عائد'), ('envoy', 'موفد'), ('returning demonstrator', 'معيد عائد'), ('loathes', 'مستنكف'), ('Transfer outside the university', 'نقل خارج الجامعة'), ('end services', 'انهاء خدمات'), ('resigned', 'انهاء بحكم المستقيل')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='fatherName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'ذكر'), ('female', 'أنثى')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='home',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='maritalStatus',
            field=models.CharField(blank=True, choices=[('married', 'متزوج'), ('unmarried', 'أعزب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='militarySituation',
            field=models.CharField(blank=True, choices=[('delayed', 'مؤجل'), ('laid off', 'مسرح')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='mobile',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$', 'accept only mobile numbers')]),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='motherName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='nominationReason',
            field=models.CharField(blank=True, choices=[('contest', 'مسابقة'), ('First graduate', 'خريج أول')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='residence',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='secion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='specialization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='telephone',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$', 'accept only mobile numbers')]),
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='university',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='alimony',
            field=models.CharField(blank=True, choices=[('grant', 'منحة'), ('seat', 'مقعد')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='atDisposalOfUniversityDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='backDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='commencementDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='defenseDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='dispatchCountry',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='dispatchEndDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='dispatchType',
            field=models.CharField(blank=True, choices=[('inner', 'داخلي'), ('outer', 'خارجي')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='dispatchUniversity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='gettingCertificateDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='innerSupervisor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='lastReport',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='lastReportDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='outerSupervisor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='requiredCertificate',
            field=models.CharField(blank=True, choices=[('language', 'لغة'), ('master', 'ماجستير'), ('ph.d', 'دكتوراه')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dispatchdecision',
            name='studentId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatchDecision', to='app.demonstrator'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='duration',
            name='dispatchDuration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatchDuration', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='extensionDuration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extensionDuration', to='app.extension'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='freezeDuration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freezeDuration', to='app.freeze'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='languageCourseDuration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='languageCourseDuration', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='duration',
            name='newDuration',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newDuration', to='app.durationchange'),
        ),
        migrations.AlterField(
            model_name='duration',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='durationchange',
            name='dispatchDecisionNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='durationChange', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='extension',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='extension',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='extension',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='extension',
            name='dispatchDecisionId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extension', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='extensionDecisionId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freeze', to='app.extension'),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='average',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='degree',
            field=models.CharField(blank=True, choices=[('diploma', 'دبلوم'), ('master', 'ماجستير'), ('ph.d', 'دكتوراه')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='section',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='specialzaion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='studentId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='graduateStudies', to='app.demonstrator'),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='university',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudies',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{4}[-][0-9]{4}$', 'in format yyyy-yyyy')]),
        ),
        migrations.AlterField(
            model_name='nominaitiondecision',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nominaitiondecision',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nominaitiondecision',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='regularizationdecision',
            name='decisionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regularizationdecision',
            name='decisionNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='regularizationdecision',
            name='decisionType',
            field=models.CharField(blank=True, choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='regularizationdecision',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='specializationchange',
            name='dispatchDecisionNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specializationChange', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='specializationchange',
            name='newSpecialization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='universitychange',
            name='dispatchDecisionNumber',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='universityChange', to='app.dispatchdecision'),
        ),
        migrations.AlterField(
            model_name='universitychange',
            name='newUniversity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='universitydegree',
            name='average',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='universitydegree',
            name='section',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='universitydegree',
            name='university',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='universitydegree',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{4}[-][0-9]{4}$', 'in format yyyy-yyyy')]),
        ),
    ]