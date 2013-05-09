# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        db.rename_table('clocker_employee1', 'clocker_employee')

        # Changing field 'Shift.employee'
        db.alter_column('Shift', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee']))

        # Changing field 'ShiftSummary.employee'
        db.alter_column('Shift Summary', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee']))

        # Delete auth User Table, but might not have ever existed.                                                                                                                              
        db.delete_table(u'auth_user_groups')                                                                                                                                                    
        db.delete_table(u'auth_user_user_permissions')
        db.delete_table(u'auth_user')                                                                                                                                                           

    def backwards(self, orm):
        pass
        # # Adding model 'Employee1'
        # db.create_table(u'clocker_employee1', (
        #     ('username', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        #     ('last_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        #     ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        #     ('has_salary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        #     (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        #     ('hourly_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
        #     ('salary', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
        #     ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        #     ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
        #     ('hire_date', self.gf('django.db.models.fields.DateField')()),
        #     ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
        #     ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        #     ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 8, 0, 0))),
        # ))
        # db.send_create_signal(u'clocker', ['Employee1'])

        # # Deleting model 'Employee'
        # db.delete_table(u'clocker_employee')


        # # Changing field 'Shift.employee'
        # db.alter_column('Shift', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee1']))

        # # Changing field 'ShiftSummary.employee'
        # db.alter_column('Shift Summary', 'employee_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clocker.Employee1']))

    models = {
        u'clocker.employee': {
            'Meta': {'object_name': 'Employee'},
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
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_in': ('django.db.models.fields.DateTimeField', [], {}),
            'time_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'clocker.shiftsummary': {
            'Meta': {'ordering': "['shift', 'employee', 'job']", 'object_name': 'ShiftSummary', 'db_table': "'Shift Summary'"},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Employee']"}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Job']"}),
            'miles': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'shift': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clocker.Shift']"})
        }
    }

    complete_apps = ['clocker']
