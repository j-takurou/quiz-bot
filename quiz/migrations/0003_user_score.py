# Generated by Django 4.0.5 on 2022-10-07 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_choice_is_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
