# Generated by Django 4.1.7 on 2023-04-03 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_alter_dispatch_dispatchbegindate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispatch',
            name='dispatchBeginDate',
        ),
    ]
