# Generated by Django 4.2 on 2023-05-15 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_structure', '0003_news_coin_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to='news_images/'),
        ),
    ]
