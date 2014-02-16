from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect
from functools import wraps
from django.utils.decorators import available_attrs

def user_has_event_perm(event_id, user_id):
	def decorator(view_func): #second wrapper gets view_func
        @wraps(view_func, assigned=available_attr(view_func))
        def wrapper(request, *args, **kwargs)
            item_id = kw.get('item_id', None)
            if item_id == parameter:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('home')
        return wrapper
    return decorator

