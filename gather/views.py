from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from gather.forms import EventForm, NewUserForm
import datetime
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from gather.models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import json
from gather import WAIT_FOR_FEEDBACK
import requests
from django.views.decorators.csrf import csrf_exempt


def event_guide(request):
	return render(request, 'gather_event_guide.html')

@login_required
def create_event(request):
	current_user = request.user
	# if the user doesn't have a proper profile, then make sure they extend it first
	# TODO FIXME This is a direct dependency on an external app (the core app where the UserProfile model lives) 
	if (not current_user.profile.bio) or (not current_user.profile.image):
		messages.add_message(request, messages.INFO, 'We want to know who you are! Please complete your profile before submitting an event.')
		return HttpResponseRedirect('/people/%s/edit/' % current_user.username)

	other_users = User.objects.exclude(id=current_user.id)
	user_list = [u.username for u in other_users]
	try:
		event_admin = Group.objects.get(name='gather_event_admin')
		if event_admin in current_user.groups.all():
			is_event_admin = True
		else:
			is_event_admin = False
	except:
		is_event_admin = False
	if request.method == 'POST':
		print request.POST
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			event = form.save(commit=False)
			event.creator = current_user
			event.save()
			co_organizers = form.cleaned_data.get('co_organizers')
			# always make sure current user is an organizer
			event.organizers.add(current_user)
			event.organizers.add(*co_organizers)
			# organizers should be attendees by default, too. 
			event.attendees.add(current_user)
			event.save()
			messages.add_message(request, messages.INFO, 'The event has been created.')
			return HttpResponseRedirect('/events/e/%s' % event.slug)
		else:
			print "form error"
			print form.errors

	else:
		form = EventForm()
	return render(request, 'gather_event_create.html', {'form': form, 'current_user': current_user, 'user_list': json.dumps(user_list), 'is_event_admin': is_event_admin})

@login_required
def edit_event(request, event_slug):
	current_user = request.user
	other_users = User.objects.exclude(id=current_user.id)
	user_list = [u.username for u in other_users]
	event = Event.objects.get(slug=event_slug)
	if not (request.user.is_authenticated() and request.user in event.organizers.all()):
		return HttpResponseRedirect("/")

	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES, instance=event)
		if form.is_valid():
			event = form.save(commit=False)
			co_organizers = form.cleaned_data.get('co_organizers')
			# always make sure current user is an organizer
			event.organizers.add(current_user)
			event.organizers.add(*co_organizers)
			event.save()
			messages.add_message(request, messages.INFO, 'The event has been saved.')
			return HttpResponseRedirect('/events/e/%s' % event.slug)
		else:
			print "form error"
			print form.errors

	else:
		# format the organizers as a string for use with the autocomplete field
		other_organizers = event.organizers.exclude(id=current_user.id)
		other_organizer_usernames = [u.username for u in other_organizers]
		other_organizer_usernames_string = ",".join(other_organizer_usernames)
		print event.organizers.all()
		form = EventForm(instance=event, initial={'co_organizers': other_organizer_usernames_string})
	return render(request, 'gather_event_edit.html', {'form': form, 'current_user': current_user, 'event_slug': event_slug, 'user_list': json.dumps(user_list)})

def view_event(request, event_slug):
	event = Event.objects.get(slug=event_slug)

	# is the event in the past?
	today = timezone.now()
	print event.end
	if event.end < today:
		past = True
	else:
		past = False

	# set up for those without accounts to RSVP
	if request.user.is_authenticated():
		current_user = request.user
		new_user_form = None
		login_form = None
		event_admin_group = Group.objects.get(name='gather_event_admin')
		if event_admin_group in current_user.groups.all(): 
			user_is_event_admin = True
		else:
			user_is_event_admin = False
	else:
		current_user = None
		new_user_form = NewUserForm()
		login_form = AuthenticationForm()
		user_is_event_admin = False

	# this is counter-intuitive - private events are viewable to those who have
	# the link. so private events are indeed shown to anyone (once they are approved). 
	if (event.status == 'live' and event.private) or event.is_viewable(current_user):
		if current_user and current_user in event.organizers.get_query_set():
			user_is_organizer = True
		else:
			user_is_organizer = False
		num_attendees = len(event.attendees.all())
		# only meaningful if event.limit > 0
		spots_remaining = event.limit - num_attendees
		event_email = 'event%d@%s' % (event.id, settings.LIST_DOMAIN)
		domain = Site.objects.get_current().domain
		return render(request, 'gather_event_view.html', {'event': event, 'current_user': current_user, 
			'user_is_organizer': user_is_organizer, 'new_user_form': new_user_form, "event_email": event_email, "domain": domain,
			'login_form': login_form, "spots_remaining": spots_remaining, 'user_is_event_admin': user_is_event_admin, 
			"num_attendees": num_attendees, 'in_the_past': past, 'endorsements': event.endorsements.all()})

	else:
		return HttpResponseRedirect('/404')


def upcoming_events(request):
	if request.user.is_authenticated():
		current_user = request.user
	else:
		current_user = None
	today = datetime.datetime.today()
	all_upcoming = Event.objects.filter(start__gte = today).order_by('start')
	culled_upcoming = []
	for event in all_upcoming:
		if event.is_viewable(current_user):
			culled_upcoming.append(event)

	# show 10 events per page
	paged_upcoming = Paginator(culled_upcoming, 10) 
	page = request.GET.get('page')
	try:
		events = paged_upcoming.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		events = paged_upcoming.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		events = paged_upcoming.page(paginator.num_pages)

	return render(request, 'gather_events_list.html', {"events": events, 'current_user': current_user, 'page_title': 'Upcoming Events'})


def user_events(request, username):
	user = User.objects.get(username=username)
	today = timezone.now()
	events_organized_upcoming = user.events_organized.all().filter(end__gte = today).order_by('start')
	events_attended_upcoming = user.events_attending.all().filter(end__gte = today).order_by('start')
	events_organized_past = user.events_organized.all().filter(end__lt = today).order_by('-start')
	events_attended_past = user.events_attending.all().filter(end__lt = today).order_by('-start')
	return render(request, 'gather_user_events_list.html', {'events_organized_upcoming': events_organized_upcoming, 
		'events_attended_upcoming': events_attended_upcoming, 
		'events_organized_past': events_organized_past, 
		'events_attended_past': events_attended_past, 
		'current_user': user, 'page_title': 'Upcoming Events'})


@login_required
def needs_review(request):
	# if user is not an event admin, redirect
	event_admin = Group.objects.get(name='gather_event_admin')
	if not request.user.is_authenticated() or (event_admin not in request.user.groups.all()):
		return HttpResponseRedirect('/')
		
	# upcoming events that are not yet live
	today = timezone.now()
	events_pending = Event.objects.filter(status=Event.PENDING).filter(end__gte = today)
	events_under_discussion = Event.objects.filter(status=Event.FEEDBACK).filter(end__gte = today)
	return render(request, 'gather_events_admin_needing_review.html', {'events_pending': events_pending, 'events_under_discussion': events_under_discussion })

def past_events(request):
	if request.user.is_authenticated():
		current_user = request.user
	else:
		current_user = None
	today = datetime.datetime.today()
	# most recent first
	all_past = Event.objects.filter(start__lt = today).order_by('-start')
	culled_past = []
	for event in all_past:
		if event.is_viewable(current_user):
			culled_past.append(event)
	# show 10 events per page
	paged_past = Paginator(culled_past, 10) 
	page = request.GET.get('page')
	try:
		events = paged_past.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		events = paged_past.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		events = paged_past.page(paginator.num_pages)

	return render(request, 'gather_events_list.html', {"events": events, 'user': current_user, 'page_title': 'Past Events'})


@login_required
def rsvp_event(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	user_id_str = request.POST.get('user_id')
	event = Event.objects.get(slug=event_slug)
	user = User.objects.get(pk=int(user_id_str))
	if user in event.organizers.all():
		user_is_organizer = True
	else:
		user_is_organizer = False
	if user not in event.attendees.all():
		event.attendees.add(user)
		event.save()
		num_attendees = event.attendees.count()
		spots_remaining = event.limit - num_attendees 
		return render(request, "snippets/rsvp_info.html", {"num_attendees": num_attendees, "spots_remaining": spots_remaining, "event": event, 'current_user': user, 'user_is_organizer': user_is_organizer });
		
	else:
		print 'user was aready attending'
	return HttpResponse(status_code=500); 


############################################
########### AJAX REQUESTS ##################

@login_required
def rsvp_cancel(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	user_id_str = request.POST.get('user_id')

	print 'event slug'
	print event_slug
	event = Event.objects.get(slug=event_slug)
	user = User.objects.get(pk=int(user_id_str))
	if user in event.organizers.all():
		user_is_organizer = True
	else:
		user_is_organizer = False

	if user in event.attendees.all():
		event.attendees.remove(user)
		event.save()
		num_attendees = event.attendees.count()
		spots_remaining = event.limit - num_attendees 
		return render(request, "snippets/rsvp_info.html", {"num_attendees": num_attendees, "spots_remaining": spots_remaining, "event": event, 'current_user': user, 'user_is_organizer': user_is_organizer });
	else:
		print 'user was not attending'
	return HttpResponse(status_code=500); 

def rsvp_new_user(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	print request.POST
	# get email signup info and remove from form, since we tacked this field on
	# but it's not part of the user model. 
	weekly_updates = request.POST.get('email-notifications')
	if weekly_updates == 'on':
		weekly_updates = True
	else:
		weekly_updates = False
	print 'weekly updates?'
	print weekly_updates

	# create new user
	form = NewUserForm(request.POST)
	if form.is_valid():
		new_user = form.save()
		new_user.save()
		notifications = new_user.event_notifications
		notifications.weekly = weekly_updates
		notifications.save()

		password = request.POST.get('password1')
		new_user = authenticate(username=new_user.username, password=password)
		login(request, new_user)
		# RSVP new user to the event
		event = Event.objects.get(slug=event_slug)
		event.attendees.add(new_user)
		print (event.attendees.all())
		event.save()
		user_msg = 'Thanks! Your account has been created. Check your email for login info and how to update your preferences.'
		return HttpResponse(json.dumps({'num_attendees': len(event.attendees.all()), 'user_id': new_user.id, 'user_msg': user_msg}), content_type='application/json')
	else:
		errors = form.errors
		return HttpResponse(json.dumps(errors))

	return HttpResponse(status_code=500); 

def endorse(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	event = Event.objects.get(slug=event_slug)

	print request.POST
	endorser = request.user
	event.endorsements.add(endorser)
	event.save()
	endorsements = event.endorsements.all()
	return render(request, "snippets/endorsements.html", {"endorsements": endorsements, "current_user": request.user});

def event_approve(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	event = Event.objects.get(slug=event_slug)
	event_admin = Group.objects.get(name='gather_event_admin')

	print request.POST
	event.status = Event.READY
	event.save()
	if event_admin in request.user.groups.all():
		user_is_event_admin = True
	else:
		user_is_event_admin = False
	if request.user in event.organizers.all():
		user_is_organizer = True
	else:
		user_is_organizer = False
	msg_success = "Success! The event has been approved."
	return render(request, "snippets/event_status_area.html", {'event': event, 'user_is_organizer': user_is_organizer, 'user_is_event_admin': user_is_event_admin})

def event_publish(request, event_slug):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')

	event = Event.objects.get(slug=event_slug)
	event_admin = Group.objects.get(name='gather_event_admin')

	print request.POST
	event.status = Event.LIVE
	event.save()
	if event_admin in request.user.groups.all():
		user_is_event_admin = True
	else:
		user_is_event_admin = False
	if request.user in event.organizers.all():
		user_is_organizer = True
	else:
		user_is_organizer = False
	msg_success = "Success! The event has been published."
	return render(request, "snippets/event_status_area.html", {'event': event, 'user_is_organizer': user_is_organizer, 'user_is_event_admin': user_is_event_admin})


def email_preferences(request, username):
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')
	
	print request.POST
	u = User.objects.get(username=username)
	notifications = u.event_notifications
	if request.POST.get('event_reminders') == 'on':
		notifications.reminders = True
	else:
		notifications.reminders = False

	if request.POST.get('weekly_updates') == 'on':
		notifications.weekly = True
	else:
		notifications.weekly = False
	notifications.save()
	return HttpResponseRedirect('/people/%s/' % u.username)



############################################
########### EMAIL ENDPOINTS ################

@csrf_exempt
def event_message(request):
	''' new messages sent to event email addresses are posed to this view '''
	if not request.method == 'POST':
		return HttpResponseRedirect('/404')
	
	print request.POST
	recipient = request.POST.get('recipient')
	sender = request.POST.get('from')
	subject = request.POST.get('subject')
	body_plain = request.POST.get('body-plain')
	body_html = request.POST.get('body-html')

	# get the event info and make sure the event exists
	# we know that the route is always in the form eventXX, where XX is the
	# event id.
	print recipient
	alias = recipient.split('@')[0]
	event_id = int(alias[5:])
	print event_id
	event = Event.objects.get(id=event_id)

	# find the event organizers and admins
	organizers = event.organizers.all()
	admin_group = Group.objects.get(name='gather_event_admin')
	admins = admin_group.user_set.all()

	# bcc list 
	bcc_list = []
	for organizer in organizers:
		if organizer.email not in bcc_list:
			bcc_list.append(organizer.email)
	for admin in admins:
		if admin.email not in bcc_list:
			bcc_list.append(admin.email)
	print bcc_list

	# prefix subject
	if subject.find('[Event Discussion') < 0:
		prefix = '[Event Discussion: %s] ' % event.slug[0:30]
		subject = prefix + subject
	print subject

	# add in footer
	domain = Site.objects.get_current().domain
	event_url = domain + '/events/%s' % event.slug
	print event_url
	footer = '''\n\n-------------------------------------------\nYou are receving this email because you are one of the organizers or an event admin at this location. Visit this event online at %s.'''% event_url
	body_plain = body_plain + footer
	body_html = body_html + footer

	return
	# send the message 
#	mailgun_api_key = settings.MAILGUN_API_KEY
#	list_domain = settings.LIST_DOMAIN
#	resp = requests.post(
#	    "https://api.mailgun.net/v2/%s/messages" % list_domain,
#	    auth=("api", mailgun_api_key),
#	    data={"from": sender,
#	          "to": [recipient, ],
#			  "bcc": bcc_list,
#	          "subject": subject,
#	          "text": body_plain,
#			  "html": body_html
#		}
#	)
#	print resp.text

	return HttpResponse(status=200)


