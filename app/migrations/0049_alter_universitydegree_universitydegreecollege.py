# Generated by Django 4.2.1 on 2023-07-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_alter_universitydegree_universitydegreecollege'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universitydegree',
            name='universityDegreeCollege',
            field=models.CharField(max_length=100),
        ),
    ]
