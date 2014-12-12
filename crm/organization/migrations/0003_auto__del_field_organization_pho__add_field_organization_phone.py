# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Organization.pho'
        db.delete_column(u'organization', 'pho_id')

        # Adding field 'Organization.phone'
        db.add_column(u'organization', 'phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Organization.pho'
        db.add_column(u'organization', 'pho',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.Phone'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Organization.phone'
        db.delete_column(u'organization', 'phone')


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
        u'organization.address': {
            'Meta': {'object_name': 'Address', 'db_table': "u'address'"},
            'apartment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'organization.designation': {
            'Meta': {'object_name': 'Designation', 'db_table': "u'designation'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'organization.organization': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Organization', 'db_table': "u'organization'"},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Address']", 'null': 'True', 'blank': 'True'}),
            'administrator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'OrgAdmin'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'blank': 'True'}),
            'designations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['organization.Designation']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['organization.OrganizationType']", 'null': 'True', 'blank': 'True'})
        },
        u'organization.organizationtype': {
            'Meta': {'object_name': 'OrganizationType', 'db_table': "u'organization_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'organization.person': {
            'Meta': {'object_name': 'Person', 'db_table': "u'person'"},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Address']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'organization.phone': {
            'Meta': {'object_name': 'Phone', 'db_table': "u'phone'"},
            'designation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Designation']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.PhoneType']", 'db_column': "u'phone_type'"})
        },
        u'organization.phonetype': {
            'Meta': {'object_name': 'PhoneType', 'db_table': "u'phone_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'organization.visitingcards': {
            'Meta': {'object_name': 'VisitingCards', 'db_table': "u'visiting_cards'"},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Address']", 'null': 'True', 'blank': 'True'}),
            'designation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'orgusermap'", 'to': u"orm['organization.Designation']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['organization.Organization']", 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['organization']