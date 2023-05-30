# Generated by Django 4.2 on 2023-05-09 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0001_initial'),
        ('users', '0003_alter_useretu_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='useretu',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='university_structure.group'),
        ),
    ]
