Gather
=======

A Django events app that supports heartwarming gatherings! Support for attendance and notifications. 

Event fields:

* start datetime
* end datetime
* title
* description
* image
* attend (yes/no/maybe)
* notifications (default = yes for attendees, may opt out)
* location (with google maps location autocomplete)
* creator 
* organizer (default = creator)
 

Intended features:

* event CRUD operations
* calendar display of events over various standard and date ranges
* template tags to show all events that a user has followed
* expose certain operations to users who have already followed an event
* message the organizer? comments?

Installation
===

* add to your requirements.txt file: `git+https://git@github.com/opendoor/django-gather.git`
* re-run pip `install -r requirements.txt`
* add `gather` to your settings.py file, under INSTALLED_APPS


Dependencies
===== 

* jquery (assumed to be included in your parent project; if not - do it)
* [timepicker jquery addon](http://trentrichardson.com/examples/timepicker/) - the required files are already included in the static dir but may need to be updated over time. 

Expectations
====== 

* expects you to have a block called {% extrajs %} in your base or main
  template file. this block should come at the bottom of the page, after your
  other javascipt includes (eg. jquery). 

