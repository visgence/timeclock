# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Timesheet.hourly_rate'
        db.add_column(u'clocker_timesheet', 'hourly_rate',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Timesheet.hourly_rate'
        db.delete_column(u'clocker_timesheet', 'hourly_rate')


    models = {
        u'clocker.employee': {
            'Meta': {'ordering': "['username']", 'object_name': 'Employee'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 18, 0, 0)'}),
            'first_name': ('django.db.models.fields.TextField', [], {}),
            'has_salary': ('django.db.models.fields.BooleanField', [], {}),
            'hire_date': ('django.db.models.fields.DateField', [], {}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.TextField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'salary': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        u'clocker.job': {
            'Meta': {'ordering': "['-is_active', 'name']", 'object_name': 'Job', 'db_table': "'Job'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'clocker.shift': {
            'Meta': {'ordering': "['-time_in', 'employee']", 'object_name': 'Shift', 'db_table': "'Shift'"},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'clocker.shiftsummary': {
            'Meta': {'ordering': "['shift', 'employee', 'job']", 'unique_together': "(('job', 'shift'),)", 'object_name': 'ShiftSummary', 'db_table': "'Shift Summary'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Job']"}),
            'miles': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Shift']"})
        },
        u'clocker.timesheet': {
            'Meta': {'ordering': "['-end']", 'object_name': 'Timesheet'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timesheet_set'", 'to': u"orm['clocker.Employee']"}),
            'end': ('django.db.models.fields.BigIntegerField', [], {}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shifts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['clocker.Shift']", 'symmetrical': 'False'}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['clocker']