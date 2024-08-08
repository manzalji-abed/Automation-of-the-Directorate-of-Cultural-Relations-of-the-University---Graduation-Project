# Generated by Django 4.1.7 on 2023-04-02 08:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_demonstrator_nominationreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch',
            name='dispatchBeginDate',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationDay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationMonth',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationYear',
            field=models.IntegerField(default=0),
        ),
    ]