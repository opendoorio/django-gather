Gather
=======

A Django events app focused on community run and community managed gatherings. 

Major features:
* Events support images, multiple organizers, organizer notes, RSVPs, RSVP
  caps, and private events. 
* The notion of site-wide event admins who can see and approve pending events,
  or propose and approve their own events
* A default workflow which seeks feedback when an event is created, in
  recognition of the decentralized approval process of many communities. 
* Event management includes the ability to endorse or "+1" an event to indicate
  passive support, to discuss an event amongst organizers and admins via an
  automatically generated email address, a pipeline for event approval for both
  approved admins and general community members, and tracking of RSVPs. 
* An email notification object which tracks and allows users to specify
  preferences both for individual event reminders (on or off), or weekly event
  reminders. 

Warnings
===
This module is not yet entirely independent of modernomad. In particular there
are certain dependencies on the url structure, template names and awareness of
reservations which shouldn't show up here. 


Installation
===

* add to your requirements.txt file: `git+https://git@github.com/opendoor/django-gather.git`
* re-run pip `install -r requirements.txt`
* add `gather` to your settings.py file, under INSTALLED_APPS
* do the necessary db updates/migrations
* manually create the event notifications object for each user by iterating through all users and accessing the event_notifications attribute of each user object
* add users as appropriate to the event_admin group (manual, for now)

Dependencies
===== 

* jquery (assumed to be included in your parent project; if not - do it)
* [timepicker jquery addon](http://trentrichardson.com/examples/timepicker/) - the required files are already included in the static dir but may need to be updated over time. 

Expectations
====== 

* expects you to have a block called {% extrajs %} in your base or main
  template file. this block should come at the bottom of the page, after your
  other javascipt includes (eg. jquery). 
* the included templates reference a base template called 'base.html' and use a
  main body block called 'content.' Of course these can and should be
  customized for any other applications. 
* mailgun integration and certain local settings included such as MAILGUN_API_KEY and LIST_DOMAIN. 
