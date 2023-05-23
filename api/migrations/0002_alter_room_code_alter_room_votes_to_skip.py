# Generated by Django 4.2.1 on 2023-05-21 20:46

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(default=api.models.generate_unique_code, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='votes_to_skip',
            field=models.IntegerField(default=1),
        ),
    ]
