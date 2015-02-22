# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0004_auto_20150216_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='redirect_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
