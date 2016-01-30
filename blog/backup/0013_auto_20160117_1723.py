# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20160115_2230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourites',
            old_name='post',
            new_name='postt',
        ),
    ]
