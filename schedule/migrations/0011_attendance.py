# Generated by Django 4.2 on 2023-05-20 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0010_alter_teacher_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата посещения')),
                ('time', models.TimeField(verbose_name='Время посещения')),
                ('presents', models.BooleanField(verbose_name='Присутствие')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
