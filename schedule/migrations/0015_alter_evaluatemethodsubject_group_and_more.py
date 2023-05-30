# Generated by Django 4.2 on 2023-05-21 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0005_alter_news_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0014_alter_evaluatemethodsubject_evaluation_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_methods', to='university_structure.group'),
        ),
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_methods', to='schedule.semester'),
        ),
        migrations.AlterField(
            model_name='evaluatemethodsubject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_methods', to='schedule.subject'),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('pass', 'Pass'), ('not_pass', 'Not Pass'), ('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory')], max_length=64)),
                ('intermediate_certification', models.BooleanField(blank=True, verbose_name='Промежуточная аттестация')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='schedule.subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]