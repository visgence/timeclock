# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Shift.employee'
        db.alter_column('Shift', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee1']))

        # Changing field 'ShiftSummary.employee'
        db.alter_column('Shift Summary', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee1']))

        # Deleting model 'Employee'
        db.delete_table('Employee')

    def backwards(self, orm):
        # Adding model 'Employee'
        db.create_table('Employee', (
            ('salary', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('hire_date', self.gf('django.db.models.fields.DateField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('has_salary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hourly_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'clocker', ['Employee'])


        # Changing field 'Shift.employee'
        db.alter_column('Shift', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee']))
        # Deleting field 'Employee1.is_active'
        db.delete_column(u'clocker_employee1', 'is_active')

        # Deleting field 'Employee1.date_joined'
        db.delete_column(u'clocker_employee1', 'date_joined')


        # Changing field 'ShiftSummary.employee'
        db.alter_column('Shift Summary', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee']))

    models = {
        u'clocker.employee1': {
            'Meta': {'object_name': 'Employee1'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 8, 0, 0)'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'has_salary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hire_date': ('django.db.models.fields.DateField', [], {}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'salary': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'clocker.job': {
            'Meta': {'ordering': "['-is_active']", 'object_name': 'Job', 'db_table': "'Job'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'clocker.shift': {
            'Meta': {'ordering': "['time_in', 'employee']", 'object_name': 'Shift', 'db_table': "'Shift'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee1']"}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'clocker.shiftsummary': {
            'Meta': {'ordering': "['shift', 'employee', 'job']", 'object_name': 'ShiftSummary', 'db_table': "'Shift Summary'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee1']"}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Job']"}),
            'miles': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Shift']"})
        }
    }

    complete_apps = ['clocker']
