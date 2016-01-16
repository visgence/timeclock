# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clocker', '0002_auto_20160115_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='billable_rate',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='budget',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
        ),
    ]
