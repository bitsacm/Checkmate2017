# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-02 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0034_auto_20170902_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='build_solved',
            field=models.CharField(default='0000000000000000000000000000000000000000000000000000000', max_length=80),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default='00000000000000000000000000000000000000000000000000000', max_length=80),
        ),
    ]