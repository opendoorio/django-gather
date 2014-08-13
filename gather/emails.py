from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
import requests

def new_event_notification(event, location):
	# notify the event admins
	admin_group = event.admin
	print 'generating new event notification'
	recipients = [admin.email for admin in admin_group.users.all()]
	event_short_title = event.title[0:50]
	if len(event.title) > 50:
		event_short_title = event_short_title + "..."
	subject = '[' + location.email_subject_prefix + ']' + " A new event has been created: %s" % event_short_title
	from_address = location.from_email()
	plaintext = get_template('emails/new_event_notify.txt')
	c = Context({
		'event': event,
		'creator': event.creator,
		'location': location,
		'location_name': location.name,
	})
	body_plain = plaintext.render(c)

	mailgun_api_key = settings.MAILGUN_API_KEY
	list_domain = settings.LIST_DOMAIN
	resp = requests.post(
		"https://api.mailgun.net/v2/%s/messages" % list_domain,
		auth=("api", mailgun_api_key),
		data={"from": from_address,
			"to": recipients,
			"subject": subject,
			"text": body_plain,
		}
	)
	print 'mailgun responded with:'
	print resp.text

def event_approved_notification(event, location):
	print 'generating email to notify organizers'
	recipients = [organizer.email for organizer in event.organizers.all()]
	subject = '[' + location.email_subject_prefix + ']' + " Your event is ready to be published"
	from_address = location.from_email()
	plaintext = get_template('emails/event_approved_notify.txt')
	c = Context({
		'event': event,
		'domain' : Site.objects.get_current().domain,
		'location_name': location.name,
	})
	body_plain = plaintext.render(c)

	mailgun_api_key = settings.MAILGUN_API_KEY
	list_domain = settings.LIST_DOMAIN
	resp = requests.post(
	    "https://api.mailgun.net/v2/%s/messages" % list_domain,
	    auth=("api", mailgun_api_key),
	    data={"from": from_address,
	          "to": recipients,
	          "subject": subject,
	          "text": body_plain,
		}
	)
	print 'mailgun responded with:'
	print resp.text


def event_published_notification(event, location):
	print 'generating email to notify organizers that event was published'
	recipients = [organizer.email for organizer in event.organizers.all()]
	event_short_title = event.title[0:50]
	if len(event.title) > 50:
		event_short_title = event_short_title + "..."
	subject = '[' + location.email_subject_prefix + ']' + " Your event is now live: %s" % event_short_title
	from_address = location.from_email()
	plaintext = get_template('emails/event_published_notify.txt')
	c = Context({
		'event': event,
		'domain' : Site.objects.get_current().domain,
		'location_name': location.name,
	})
	body_plain = plaintext.render(c)

	mailgun_api_key = settings.MAILGUN_API_KEY
	list_domain = settings.LIST_DOMAIN
	resp = requests.post(
	    "https://api.mailgun.net/v2/%s/messages" % list_domain,
	    auth=("api", mailgun_api_key),
	    data={"from": from_address,
	          "to": recipients,
	          "subject": subject,
	          "text": body_plain,
		}
	)
	print 'mailgun responded with:'
	print resp.text




