# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_id', models.TextField()),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('starts', models.FloatField()),
                ('review_count', models.FloatField()),
                ('categories', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_id', models.TextField()),
                ('categories', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LDADict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_id', models.TextField()),
                ('word', models.TextField()),
                ('score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_id', models.TextField()),
                ('business_id', models.TextField()),
                ('topic_id', models.TextField()),
                ('score', models.FloatField()),
            ],
        ),
    ]
