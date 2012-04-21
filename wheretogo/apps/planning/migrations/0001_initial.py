# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table('planning_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('planning', ['Place'])

        # Adding model 'Planning'
        db.create_table('planning_planning', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plannings', to=orm['profiles.FacebookProfile'])),
            ('lat', self.gf('django.db.models.fields.FloatField')(default=50.435462778)),
            ('lon', self.gf('django.db.models.fields.FloatField')(default=30.48955857)),
            ('radius', self.gf('django.db.models.fields.FloatField')(default=10000)),
        ))
        db.send_create_signal('planning', ['Planning'])

        # Adding M2M table for field profiles on 'Planning'
        db.create_table('planning_planning_profiles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('planning', models.ForeignKey(orm['planning.planning'], null=False)),
            ('facebookprofile', models.ForeignKey(orm['profiles.facebookprofile'], null=False))
        ))
        db.create_unique('planning_planning_profiles', ['planning_id', 'facebookprofile_id'])

        # Adding model 'PlanningResultPlace'
        db.create_table('planning_planningresultplace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('planning', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planning.Planning'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planning.Place'])),
            ('rank', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('planning', ['PlanningResultPlace'])

    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table('planning_place')

        # Deleting model 'Planning'
        db.delete_table('planning_planning')

        # Removing M2M table for field profiles on 'Planning'
        db.delete_table('planning_planning_profiles')

        # Deleting model 'PlanningResultPlace'
        db.delete_table('planning_planningresultplace')

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
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'planning.planning': {
            'Meta': {'object_name': 'Planning'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '50.435462778'}),
            'lon': ('django.db.models.fields.FloatField', [], {'default': '30.48955857'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plannings'", 'to': "orm['profiles.FacebookProfile']"}),
            'profiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'planning_involved_in'", 'symmetrical': 'False', 'to': "orm['profiles.FacebookProfile']"}),
            'radius': ('django.db.models.fields.FloatField', [], {'default': '10000'})
        },
        'planning.planningresultplace': {
            'Meta': {'object_name': 'PlanningResultPlace'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planning.Place']"}),
            'planning': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planning.Planning']"}),
            'rank': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'profiles.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'fid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['planning']