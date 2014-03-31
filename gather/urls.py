from django.conf.urls import patterns, include, url
from django.conf import settings
import registration.backends.default.urls

urlpatterns = patterns('',
	url(r'^create/$', 'gather.views.create_event', name='create_event'),
	url(r'^upcoming/$', 'gather.views.upcoming_events', name='upcoming_events'),
	url(r'^guide/$', 'gather.views.event_guide', name='event_guide'),
	url(r'^past/$', 'gather.views.past_events', name='past_events'),
	url(r'^review/$', 'gather.views.needs_review', name='needs_review'),
	url(r'^message/$', 'gather.views.event_message', name='event_message'),
	url(r'newuser/$', 'gather.views.new_user_email_signup', name='new_user_email_signup'),
    url(r'^emailpreferences/(?P<username>[\w\d\-\.@+_]+)/$', 'gather.views.email_preferences', name='email_preferences'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/edit/$', 'gather.views.edit_event', name='edit_event'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/rsvp/yes/newuser/$', 'gather.views.rsvp_new_user', name='rsvp_new_user'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/rsvp/no/$', 'gather.views.rsvp_cancel', name='rsvp_cancel'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/rsvp/yes/$', 'gather.views.rsvp_event', name='rsvp_event'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/endorse/$', 'gather.views.endorse', name='event_endorse'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/publish/$', 'gather.views.event_publish', name='event_publish'),
	url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/approve/$', 'gather.views.event_approve', name='event_approve'),
    url(r'^(?P<event_id>\d+)/(?P<event_slug>[\w\d\-\.@+_]+)/$', 'gather.views.view_event', name='view_event'),
)




