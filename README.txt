# Advanced Search Filter

This is a Django *Application* intended to provided a mechanism for users to
search on individual fields of the change lists associated model. It also
provides a way to specify a date field as a 'date from' and another as a
'date to' field.

It's integration with Django admin is a bit "hackish" for two reasons:

  1. it inserts itself into the date hierarchy block in the change list form
     template, doing so because there isn't another suitable block that it can
     be inserted into and still look "decent"
  2. it uses javascript to redirect the page to the same page, but with
     querystring values appropriate for the search. This is because the
     "advanced search" functionality is provided by a django template
     tag/filter, which cannot redirect the request from the backend


## Requirements

  * **Browsers:** should work on IE9+ and most versions of other
    browsers. Makes use of DOMContentLoaded, window.location.href,
    document.body.style.display, innerHTML, addEventListener, and querySelector
  * **Django 1.5** (at least, that's the version it was developed for)
  * **Django Contrib Admin**


## Usage

First, download/install the app and add it to your settings (also making sure
that the django.contrib.admin is installed and activated):

    INSTALLED_APPS = (
        # ...
        'django.contrib.admin',
        #...
        'advancedsearchfilter',
        # ...
    )

You will also need to make sure that you have the `django.core.context_processors.request`
context processor added to your `TEMPLATE_CONTEXT_PREPROCESSOR` setting in your
settings.py file.

Then create a `django.forms.ModelForm` that defines the form
to be displayed for searching. If this form contains a *Meta* class with a
`date_from` or a `date_to` (or both) string property, then it uses the value
of the string to identify a date field on the model it should use the `__gte`
or `__lte` query filter on.

After that, extend the `advancedsearchfilter/change_list.html` template in your own
`templates/admin/change_list.html` (or equivalent):

    {% extends 'advancedsearchfilter/change_list.html' %}

And then, add something like the following to your template:

    {% block date_hierarchy %}
        {% with adv_search_form_class="fully.qualified.ModelFormName" %}
            {{block.super}}
        {% endwith %}
    {% endblock %}

where the 'fully.qualified.ModelFormName' is the fully qualified object name
of the ModelForm class you created.

Or, alternatively, if you want to extend from a different change list, you can
manually add the contents of the
`templates/advancedsearchfilter/change_list.html` file to your change list
template. You'll want to change the following line in your change list:

    {% block date_hierarchy %}{{ block.super }} {% advanced_search adv_search_form_class %}{% endblock %}

to something like:

    {% block date_hierarchy %}
        {% with adv_search_form_class="fully.qualified.ModelFormName" %}
            {{block.super}}
        {% endwith %}
    {% endblock %}

where the 'fully.qualified.ModelFormName' is the fully qualified object name
of the ModelForm class you created.


## Other Contributors

Sponsor: Wildcard Corp. (http://www.wildcardcorp.com)
