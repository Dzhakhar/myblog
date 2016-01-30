# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20160111_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='q',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
