# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='author',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AddField(
            model_name='favourites',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
