# Generated by Django 4.1.4 on 2023-03-18 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_demonstrator_college_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demonstrator',
            name='birthDate',
            field=models.DateField(default='2000-02-02'),
        ),
    ]