# Generated by Django 4.0.1 on 2022-01-26 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.RemoveField(
            model_name='user',
            name='c_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
    ]