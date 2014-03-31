from celery.task.schedules import crontab
from celery.task import periodic_task
from __future__ import absolute_import
from celery import shared_task
from gather.models import Event, EventNotifications
from django.contrib.auth.models import User
import json
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import Context
from django.core import urlresolvers
from django.core.mail import EmailMultiAlternatives
import requests, pytz, datetime
from django.db.models import Q
from itertools import chain

weekday_number_to_name = {
	0: "Monday",
	1: "Tuesday",
	2: "Wednesday",
	3: "Thursday",
	4: "Friday",
	5: "Saturday",
	6: "Sunday"
}


def send_events_list(user, event_list):
	domain = 'https://'+Site.objects.get_current().domain
	profile_url = domain + '/people/%s/' % user.username
	footer = 'You are receiving this email because your preferences for event reminders are on. To turn them off, visit %s' % profile_url
	sender = settings.DEFAULT_FROM_EMAIL
	subject = settings.EMAIL_SUBJECT_PREFIX + 'Reminder of your events today'
	current_tz = timezone.get_current_timezone()
	today_local = timezone.now().astimezone(current_tz).date()
	day_of_week = weekday_number_to_name[today_local.weekday()]
	plaintext = get_template('emails/events_today.txt')
	c = Context({
			'user': user,
			'events': event_list,
			'location_name': settings.LOCATION_NAME,
			'domain': domain,
			"footer": footer,
			"day_of_week": day_of_week
			})
	text_content = plaintext.render(c)
	list_domain = settings.LIST_DOMAIN

	resp = requests.post("https://api.mailgun.net/v2/%s/messages" % list_domain,
		auth=("api", settings.MAILGUN_API_KEY),
		data={
			"from": sender,
			"to": user.email,
			"subject": subject,
			"text": text_content,
		}
	)
	print resp.text

def weekly_reminder_email(user, event_list):
	domain = 'https://'+Site.objects.get_current().domain
	profile_url = domain + '/people/%s/' % user.username
	location_name = settings.LOCATION_NAME
	current_tz = timezone.get_current_timezone()
	today_local = timezone.now().astimezone(current_tz).date()
	tomorrow_local = today_local + datetime.timedelta(days=1)
	week_name = tomorrow_local.strftime("%B %d, %Y")
	footer = 'You are receiving this email because you requested weekly updates of upcoming events from %s. To turn them off, visit %s' % (location_name, profile_url)
	sender = settings.DEFAULT_FROM_EMAIL
	subject = settings.EMAIL_SUBJECT_PREFIX + 'Upcoming events for the week of %s' % week_name
	current_tz = timezone.get_current_timezone()
	today_local = timezone.now().astimezone(current_tz).date()
	plaintext = get_template('emails/events_this_week.txt')
	htmltext = get_template('emails/events_this_week.html')
	
	c_text = Context({
			'user': user,
			'events': event_list,
			'location_name': location_name,
			'domain': domain,
			"footer": footer,
			"week_name": week_name
			})
	text_content = plaintext.render(c_text)

	c_html = Context({
			'user': user,
			'events': event_list,
			'location_name': location_name,
			'domain': domain,
			"footer": footer,
			"week_name": week_name
			})
	html_content = htmltext.render(c_html)

	list_domain = settings.LIST_DOMAIN
	resp = requests.post("https://api.mailgun.net/v2/%s/messages" % list_domain,
		auth=("api", settings.MAILGUN_API_KEY),
		data={
			"from": sender,
			"to": user.email,
			"subject": subject,
			"text": text_content,
			"html": html_content,
		}
	)
	print resp.text

def events_pending():
	# events seeking feeddback and waiting for review
	pending = Event.objects.filter(start__gt = timezone.now()).filter(status='waiting for approval')
	feedback = Event.objects.filter(start__gt = timezone.now()).filter(status='seeking feedback')
	ret = {'pending': pending, 'feedback': feedback}
	return ret

def published_events_this_week_local():
	# we have to do a bunch of tomfoolery here because we want to gets events
	# that are "this week" in this week's timezone, but dates are stored in UTC which
	# is offset from the current timezone's hours by a certain amount. 
	current_tz = timezone.get_current_timezone()
	today_local = timezone.now().astimezone(current_tz).date()
	tomorrow_local = today_local + datetime.timedelta(days=1)
	seven_days_from_now_local = today_local + datetime.timedelta(days=7)
	utc_tz = pytz.timezone('UTC')
	week_local_start_time = datetime.datetime(tomorrow_local.year, tomorrow_local.month, tomorrow_local.day, 0,0)
	week_local_end_time = datetime.datetime(seven_days_from_now_local.year, seven_days_from_now_local.month, seven_days_from_now_local.day, 23,59,59)
	week_local_start_aware = timezone.make_aware(week_local_start_time, current_tz)
	week_local_end_aware = timezone.make_aware(week_local_end_time, current_tz)
	week_local_start_utc = utc_tz.normalize(week_local_start_aware.astimezone(utc_tz))
	week_local_end_utc = utc_tz.normalize(week_local_end_aware.astimezone(utc_tz))

	# get events happening today that are live
	starts_this_week_local = Event.objects.filter(start__gte =
		week_local_start_utc).filter(start__lte=week_local_end_utc).filter(status='live')
	ends_this_week_local = Event.objects.filter(end__gte =
		week_local_start_utc).filter(end__lte=week_local_end_utc).filter(status='live')
	across_this_week_local = Event.objects.filter(start__lte =
		week_local_start_utc).filter(end__gte=week_local_end_utc).filter(status='live')

	events_this_week_local = list(set(chain(starts_this_week_local, ends_this_week_local, across_this_week_local)))
	return events_this_week_local

def published_events_today_local():
	# we have to do a bunch of tomfoolery here because we want to gets events
	# that are "today" in today's timezone, but dates are stored in UTC which
	# is offset from the current timezone's hours by a certain amount. 
	current_tz = timezone.get_current_timezone()
	today_local = timezone.now().astimezone(current_tz).date()
	utc_tz = pytz.timezone('UTC')
	today_local_start_time = datetime.datetime(today_local.year, today_local.month, today_local.day, 0,0)
	today_local_end_time = datetime.datetime(today_local.year, today_local.month, today_local.day, 23,59,59)
	today_local_start_aware = timezone.make_aware(today_local_start_time, current_tz)
	today_local_end_aware = timezone.make_aware(today_local_end_time, current_tz)
	today_local_start_utc = utc_tz.normalize(today_local_start_aware.astimezone(utc_tz))
	today_local_end_utc = utc_tz.normalize(today_local_end_aware.astimezone(utc_tz))

	# get events happening today that are live
	starts_today_local = Event.objects.filter(start__gte =
		week_local_start_utc).filter(start__lte=week_local_end_utc).filter(status='live')
	ends_today_local = Event.objects.filter(end__gte =
		week_local_start_utc).filter(end__lte=week_local_end_utc).filter(status='live')
	across_today_local = Event.objects.filter(start__lte =
		week_local_start_utc).filter(end__gte=week_local_end_utc).filter(status='live')

	events_today_local = list(set(chain(starts_today_local, ends_today_local, across_today_local)))
	return events_today_local

@shared_task
@periodic_task(run_every=crontab(hour=4, minute=35))
def events_today_reminder():
	
	events_today_local = published_events_today_local()
	# for each event, 
	#	for each attendee or organizer
	#		if they want reminders, append this event to a list of reminders for today, for that person. 
	reminders_per_person = {}
	for event in events_today_local:
		distinct_event_people = list(set(list(event.attendees.all()) + list(event.organizers.all())))
		for user in distinct_event_people:
			if user.event_notifications.reminders == True and user not in reminders_per_person.keys():
				reminders_this_person = reminders_per_person.get(user, [])
				reminders_this_person.append(event)
				reminders_per_person[user] = reminders_this_person
	
	for user, events_today in reminders_per_person.iteritems():
		send_events_list(user, events_today)
	
@shared_task
@periodic_task(run_every=crontab(day_of_week='sun', hour=4, minute=30))
def weekly_upcoming_events():
	events_this_week = published_events_this_week_local()
	if len(events_this_week) == 0:
		print 'no events this week; skipping email notification'
		return
	print events_this_week
	# for each event, 
	#	for each attendee or organizer
	#		if they want reminders, append this event to a list of reminders for today, for that person. 
	weekly_notifications_on = EventNotifications.objects.filter(weekly=True)
	remindees = [notify.user for notify in weekly_notifications_on]
	
	print remindees
	for user in remindees:
		weekly_reminder_email(user, events_this_week)


