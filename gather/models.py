from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image
import uuid, os, datetime
from django.conf import settings
from django.db.models.signals import post_save
import requests

def event_img_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    # rename file to random string
    filename = "%s.%s" % (uuid.uuid4(), ext.lower())

    upload_path = "data/events/%s/" % instance.slug
    upload_abs_path = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.exists(upload_abs_path):
        os.makedirs(upload_abs_path)
    return os.path.join(upload_path, filename)

class EventManager(models.Manager):
	def upcoming(self, upto=3, current_user=None):
		# return the events happening today or in the future, returning up to
		# the number of events specified in the 'upto' argument. 
		today = datetime.date.today()
		upcoming = super(EventManager, self).get_query_set().filter(end__gte = today).order_by('start')
		print upcoming
		viewable_upcoming = []
		for event in upcoming:
			if event.is_viewable(current_user):
				viewable_upcoming.append(event)
				if len(viewable_upcoming) == upto:
					break
		print viewable_upcoming
		return viewable_upcoming

# Create your models here.
class Event(models.Model):
	PENDING = 'waiting for approval'
	FEEDBACK = 'seeking feedback'
	READY = 'ready to publish'
	LIVE = 'live'

	event_statuses = (
			(PENDING, 'Waiting for Approval'),
			(FEEDBACK, 'Seeking Feedback'),
			(READY, 'Ready to publish'),
			(LIVE, 'Live'),
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	start = models.DateTimeField(verbose_name="Start time")
	end = models.DateTimeField(verbose_name="End time")
	title = models.CharField(max_length=300)
	slug = models.CharField(max_length=60, help_text="This will be auto-suggested based on the event title, but feel free to customize it.", unique=True)
	description = models.TextField(help_text="Basic HTML markup is supported for your event description.")
	image = models.ImageField(upload_to=event_img_upload_to)
	attendees = models.ManyToManyField(User, related_name="events_attending", blank=True, null=True)  
	notifications = models.BooleanField(default = True)
	location = models.CharField(max_length=500, help_text="Either a specific room at this location or an address if elsewhere")
	creator = models.ForeignKey(User, related_name="events_created")
	organizers = models.ManyToManyField(User, related_name="events_organized", blank=True, null=True)
	organizer_notes = models.TextField(blank=True, null=True, help_text="These will only be visible to other organizers")
	limit = models.IntegerField(default=0, help_text="Specify a cap on the number of RSVPs, or 0 for no limit.", blank=True)
	# public events can be seen by anyone, private events can only be seen by organizers and attendees. 
	private = models.BooleanField(default=False, help_text="Private events will only be seen by organizers, attendees, and those who have the link. It will not be displayed in the public listing.") 
	status = models.CharField(choices = event_statuses, default=PENDING, max_length=200, verbose_name='Review Status', blank=True)
	endorsements = models.ManyToManyField(User, related_name="events_endorsed", blank=True, null=True)

	objects = EventManager()

	def __unicode__(self):
		return self.title

	def is_viewable(self, current_user):
		# an event is viewable only if it's both live and public, or the
		# current_user is an event admin, created the event, or is an attendee
		# or organizer. 
		event_admin = Group.objects.get(name='gather_event_admin')
		if (current_user) and (event_admin in current_user.groups.all()):
			is_event_admin = True
		else:
			is_event_admin = False
		if ((self.status == 'live' and self.private == False) or (is_event_admin or 
				current_user == self.creator or current_user in self.organizers.all() or 
				current_user in self.attendees.all())):
			viewable = True
		else:
			viewable = False
		return viewable


def default_event_status(sender, instance, created, using, **kwargs):
	print instance
	print created
	print instance.status
	if created == True:
		event_admin = Group.objects.get(name='gather_event_admin')
		if event_admin in instance.creator.groups.all():
			instance.status = Event.FEEDBACK
		else:
			instance.status = Event.PENDING
post_save.connect(default_event_status, sender=Event)
	

def create_route(route_name, route_pattern, path):

	mailgun_api_key = settings.MAILGUN_API_KEY
	list_domain = settings.LIST_DOMAIN
	# strip the initial slash 
	forward_url = os.path.join(list_domain, path)
	forward_url = "https://" + forward_url
	print forward_url
	print list_domain
	expression = "match_recipient('%s')" % route_pattern
	print expression
	forward_url = "forward('%s')" % forward_url
	print forward_url
	return requests.post( "https://api.mailgun.net/v2/routes", 
			auth=("api", mailgun_api_key), 
			data={"priority": 1,
				"description": route_name,
				# the route pattern is a string but still needs to be quoted
				"expression": expression,
				"action": forward_url,
			}
	)

def create_event_email(sender, instance, created, using, **kwargs):
	if created == True:
		# XXX TODO should probably hash the ID or name of the event so we're
		# not info leaking here, if we care?
		route_pattern = "event%d" % instance.id
		route_name = 'Event %d' % instance.id
		path = "events/message/"
		resp = create_route(route_name, route_pattern, path)
		print resp.text
post_save.connect(create_event_email, sender=Event)

class EventNotifications(models.Model):
	user = models.OneToOneField(User, related_name='event_notifications')
	# send reminders on day-of the event?
	reminders = models.BooleanField(default=True)
	# receive weekly announcements about upcoming events? 
	weekly = models.BooleanField(default=False)

User.event_notifications = property(lambda u: EventNotifications.objects.get_or_create(user=u)[0])

# override the save method of the User model to create the EventNotifications
# object automatically for new users
def add_user_event_notifications(sender, instance, created, using, **kwargs):
	# just accessing the field will create the object, since the field is
	# defined with get_or_create, above. 
	instance.event_notifications
	return
	
post_save.connect(add_user_event_notifications, sender=User)





