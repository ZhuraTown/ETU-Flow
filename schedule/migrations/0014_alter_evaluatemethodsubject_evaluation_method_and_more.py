# Generated by Django 4.2 on 2023-05-21 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0005_alter_news_image'),
        ('schedule', '0013_evaluatemethodsubject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='evaluation_method',
            field=models.CharField(choices=[('exam', 'Exam'), ('offset', 'Offset')], default='exam', max_length=16),
        ),
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_method', to='university_structure.group'),
        ),
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_method', to='schedule.semester'),
        ),
    ]
