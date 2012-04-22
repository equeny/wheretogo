# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Planning.status'
        db.add_column('planning_planning', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Planning.status'
        db.delete_column('planning_planning', 'status')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'planning.place': {
            'Meta': {'object_name': 'Place'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'likes_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '-1'}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'planning.planning': {
            'Meta': {'object_name': 'Planning'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '50.435462778'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '30.48955857'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': "orm['profiles.FacebookProfile']"}),
            'profiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'planning_involved_in'", 'symmetrical': 'False', 'to': "orm['profiles.FacebookProfile']"}),
            'radius': ('django.db.models.fields.FloatField', [], {'default': '10000'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'planning.planningresultplace': {
            'Meta': {'ordering': "('-category_rank',)", 'unique_together': "(('planning', 'place'),)", 'object_name': 'PlanningResultPlace'},
            'category_rank': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes_rank': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planning.Place']"}),
            'planning': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planning.Planning']"}),
            'rank': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'profiles.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'categories_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'categories_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changes': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_friends_update': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'fb_user'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['planning']