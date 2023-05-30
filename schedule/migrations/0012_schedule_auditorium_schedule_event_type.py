# Generated by Django 4.2 on 2023-05-21 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='auditorium',
            field=models.CharField(blank=True, max_length=128, verbose_name='Аудитория'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='event_type',
            field=models.CharField(choices=[('0', 'Lecture'), ('1', 'Practice')], default='0', max_length=64, verbose_name='Лекция/практика'),
        ),
    ]
