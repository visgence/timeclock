# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('hire_date', models.DateField(verbose_name=b'date employee was hired')),
                ('has_salary', models.BooleanField(default=False)),
                ('hourly_rate', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('salary', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('username', models.TextField(unique=True)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2016, 1, 15, 21, 8, 57, 224495))),
                ('color', models.CharField(max_length=32, blank=True)),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(verbose_name=b'job name')),
                ('description', models.TextField(verbose_name=b'job description')),
                ('is_active', models.BooleanField()),
            ],
            options={
                'ordering': ['-is_active', 'name'],
                'db_table': 'Job',
            },
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_in', models.DateTimeField(verbose_name=b'clock in time')),
                ('time_out', models.DateTimeField(null=True, verbose_name=b'clock out time', blank=True)),
                ('hours', models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ['-time_in', 'employee'],
                'db_table': 'Shift',
            },
        ),
        migrations.CreateModel(
            name='ShiftSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField(verbose_name=b'total hours')),
                ('miles', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('note', models.TextField(verbose_name=b'notes about job', blank=True)),
                ('employee', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
                ('job', models.ForeignKey(to='clocker.Job', on_delete=models.PROTECT)),
                ('shift', models.ForeignKey(to='clocker.Shift', on_delete=models.PROTECT)),
            ],
            options={
                'ordering': ['shift', 'employee', 'job'],
                'db_table': 'Shift Summary',
            },
        ),
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.BigIntegerField()),
                ('end', models.BigIntegerField()),
                ('hourly_rate', models.DecimalField(max_digits=5, decimal_places=2)),
                ('signature', models.TextField(blank=True)),
                ('employee', models.ForeignKey(related_name='timesheet_set', to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
                ('shifts', models.ManyToManyField(to='clocker.Shift')),
            ],
            options={
                'ordering': ['-end'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='shiftsummary',
            unique_together=set([('job', 'shift')]),
        ),
    ]
