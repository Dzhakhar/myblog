# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_q'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='q',
            field=models.IntegerField(default=b''),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL),
        ),
    ]
