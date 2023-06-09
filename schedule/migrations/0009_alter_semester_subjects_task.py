# Generated by Django 4.2 on 2023-05-20 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0005_alter_news_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0008_rename_subject_teacher_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='semesters', to='schedule.subject', verbose_name='Предметы'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('date_of_completion', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='tasks/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='university_structure.group')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='schedule.subject')),
            ],
        ),
    ]
