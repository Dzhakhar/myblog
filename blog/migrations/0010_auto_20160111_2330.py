# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20160111_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='q',
            field=models.IntegerField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=b'', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
