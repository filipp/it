# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Note'
        db.delete_table(u'it_note')

        # Adding model 'Issue'
        db.create_table(u'it_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'it', ['Issue'])

        # Adding field 'Asset.name'
        db.add_column(u'it_asset', 'name',
                      self.gf('django.db.models.fields.CharField')(default='New Asset', max_length=256),
                      keep_default=False)

        # Adding field 'Asset.ip_address'
        db.add_column(u'it_asset', 'ip_address',
                      self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15),
                      keep_default=False)

        # Adding M2M table for field issues on 'Asset'
        m2m_table_name = db.shorten_name(u'it_asset_issues')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('asset', models.ForeignKey(orm[u'it.asset'], null=False)),
            ('issue', models.ForeignKey(orm[u'it.issue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['asset_id', 'issue_id'])

        # Deleting field 'Task.priority'
        db.delete_column(u'it_task', 'priority')

        # Adding field 'Task.issue'
        db.add_column(u'it_task', 'issue',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['it.Issue'], null=True),
                      keep_default=False)

        # Adding field 'Task.step'
        db.add_column(u'it_task', 'step',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Note'
        db.create_table(u'it_note', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'it', ['Note'])

        # Deleting model 'Issue'
        db.delete_table(u'it_issue')

        # Deleting field 'Asset.name'
        db.delete_column(u'it_asset', 'name')

        # Deleting field 'Asset.ip_address'
        db.delete_column(u'it_asset', 'ip_address')

        # Removing M2M table for field issues on 'Asset'
        db.delete_table(db.shorten_name(u'it_asset_issues'))

        # Adding field 'Task.priority'
        db.add_column(u'it_task', 'priority',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Task.issue'
        db.delete_column(u'it_task', 'issue_id')

        # Deleting field 'Task.step'
        db.delete_column(u'it_task', 'step')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'it.asset': {
            'Meta': {'object_name': 'Asset'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'default': "''", 'max_length': '15'}),
            'issues': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['it.Issue']", 'null': 'True', 'symmetrical': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'New Asset'", 'max_length': '256'})
        },
        u'it.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'it.issue': {
            'Meta': {'object_name': 'Issue'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'it.task': {
            'Meta': {'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['it.Issue']", 'null': 'True'}),
            'step': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'metoo'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['it']