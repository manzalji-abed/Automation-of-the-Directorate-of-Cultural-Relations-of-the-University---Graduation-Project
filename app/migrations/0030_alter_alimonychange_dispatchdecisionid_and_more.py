# Generated by Django 4.1.4 on 2023-03-18 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_alimonychange_dispatchdecisionid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimonychange',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alimonyChange', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='alimonychange',
            name='newAlimony',
            field=models.CharField(choices=[('grant', 'منحة'), ('seat', 'مقعد')], max_length=25),
        ),
        migrations.AlterField(
            model_name='durationchange',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='durationChange', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='durationchange',
            name='durationChangeDurationDay',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='durationchange',
            name='durationChangeDurationMonth',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='durationchange',
            name='durationChangeDurationYear',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='extension',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extension', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDecisionDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDecisionNumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDecisionType',
            field=models.CharField(choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDurationDay',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDurationMonth',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='extension',
            name='extensionDurationYear',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freeze', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDecisionDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDecisionNumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDecisionType',
            field=models.CharField(choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDurationDay',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDurationMonth',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='freeze',
            name='freezeDurationYear',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='regularization',
            name='regularizationDecisionDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='regularization',
            name='regularizationDecisionNumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='regularization',
            name='regularizationDecisionType',
            field=models.CharField(choices=[('s', 'ش.ع'), ('o', 'و'), ('b', 'ب')], max_length=10),
        ),
        migrations.AlterField(
            model_name='report',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='report',
            name='report',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='reportDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='specializationchange',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specializationChange', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='specializationchange',
            name='newSpecialization',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='universitychange',
            name='dispatchDecisionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='universityChange', to='app.dispatch'),
        ),
        migrations.AlterField(
            model_name='universitychange',
            name='newUniversity',
            field=models.CharField(max_length=100),
        ),
    ]
