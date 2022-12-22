# Generated by Django 3.2 on 2022-12-22 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fio',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]