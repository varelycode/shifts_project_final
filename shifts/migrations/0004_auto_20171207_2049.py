# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_topic_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupShift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('group_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='topic',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='boards.GroupShift'),
        ),
        migrations.DeleteModel(
            name='Board',
        ),
    ]
