# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.location'
        db.add_column('gather_event', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Location']),
                      keep_default=False)

        # Adding field 'Event.series'
        db.add_column('gather_event', 'series',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['gather.EventSeries']),
                      keep_default=False)

        # Adding field 'Event.admin'
        db.add_column('gather_event', 'admin',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='events', to=orm['gather.EventAdminGroup']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.location'
        db.delete_column('gather_event', 'location_id')

        # Deleting field 'Event.series'
        db.delete_column('gather_event', 'series_id')

        # Deleting field 'Event.admin'
        db.delete_column('gather_event', 'admin_id')


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
        'core.location': {
            'Meta': {'object_name': 'Location'},
            'about_page': ('django.db.models.fields.TextField', [], {}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'default_from_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email_subject_prefix': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'front_page_participate': ('django.db.models.fields.TextField', [], {}),
            'front_page_stay': ('django.db.models.fields.TextField', [], {}),
            'house_access_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'house_admins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'house_admin'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailgun_api_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mailgun_domain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'max_reservation_days': ('django.db.models.fields.IntegerField', [], {'default': '14'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'residents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'residences'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'stay_page': ('django.db.models.fields.TextField', [], {}),
            'stripe_public_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stripe_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'welcome_email_days_ahead': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'gather.event': {
            'Meta': {'object_name': 'Event'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['gather.EventAdminGroup']"}),
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_attending'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events_created'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'endorsements': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_endorsed'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']"}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organizer_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_organized'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': "orm['gather.EventSeries']"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'waiting for approval'", 'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'gather.eventadmingroup': {
            'Meta': {'object_name': 'EventAdminGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']", 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'gather.eventnotifications': {
            'Meta': {'object_name': 'EventNotifications'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'event_notifications'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'weekly': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gather.eventseries': {
            'Meta': {'object_name': 'EventSeries'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'gather.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['gather']