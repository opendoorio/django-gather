
## Gather

This release offers a major new events feature! The other major part of this
release was a total redesign of the layout, color scheme, and fonts of the
site, with an upgrade to bootstrap 3 and better (though still not great) mobile
compatibility. 


## Event Features

In addition to the basics of start and end times, image, description, and location, events also offer these potentially useful features:


   * Event **size limit and RSVP caps**
   * **Private events** which do not show up in the public event listing and are only visible to organizers and those have the link. One someone has RSVPed, this event will show up in their event listings.  
   * The ability to assign **multiple organizers** to an event
   * **Organizer notes** which are only visible to other co-organizers
   * **Email notification preferences** on a per user basis. Users can opt in
     or out of receiving day-of event reminders for events they have RSVP-ed
     for, as well as weekly event announcement emails for all upcoming events
     that week. 

## Accessing Event Features
 

The main page contains upcoming events, the Events menu has options to see past
or upcoming events, or to create a new event. Your personal menu let’s you see
“My events” and the Admin menu (for those who are house admins) will show you a
link to “Pending events.”

Event workflow: events can be in 4 states:  

   * Waiting for approval
   * Seeking Feedback
   * Ready to Publish
   * Live. 


Residents (and anyone else we want) are part of a group that have event admin
privileges. When event admins create a new event, it goes immediately into the
“seeking feedback” state. An event admin can publish their event and make it
live at any time, but the norm is that they give a few days for other event
admins and event co-organizers to give feedback. 

Anyone can propose events on our website. If you are not an admin, then when
you propose an event it goes into the “waiting for approval” state. An
organizer who is not an admin cannot publish an event live until an admin
approves it. 

## Feedback

There are several mechanisms for feedback. 

   * **Endorsements** are the little heart you see in the yellow admin area of an event, before it is live. Clicking on the heart is a passive way of endorsing the event. You can click the drop down menu next to a heart and see who else has endorsed it. 
   * **Email address:** each email address has its own custom email address. Emailing this address will automatically create a discussion between site-wide event admins and the co-organizers of this event.  
   * **Out of band:** we’re humans. talk to each other!


## Visibility to Others

Unless an event is live, it is generally not visible to other users and will
not show up in the upcoming or past events lists.  There are a few exceptions
to this. 


   * **Admins:** If you are an event admin, you will see all events. 
   * **Organizers:** If you are an organizer of an event that is not yet live, you will also see it in the event listings. 
   * **Private Events:** If you are an organizer or have RSVP-ed to a private event, you will see it in the event listings. 

## Notifications

(Currently this piece is built into the parent modernomad django app).
Residents and guests receive an automatic daily email informing them of
upcoming guests and events so that they are in the know about what is happening
at the house. 

## Desired Future Features

   * recurring events
   * events series
   * eventbrite or Facebook integration
   * your ideas here...


 

