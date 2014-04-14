from django.forms import fields
from django.forms import models
from django.template import Library
from django.utils.http import urlquote_plus
import importlib


register = Library()


#
# NOTE: BooleanField form fields are expected to have a *Select* widget which
#       provides 3 values: a True/'yes' field, a False/'no' field, and an
#       Any/'any' field (IE both True and False values are acceptable)
#


@register.inclusion_tag('admin/advanced_search.html', takes_context=True)
def advanced_search(context, searchform):
    request = context['request']
    form = None
    redirect = ''

    # assume the last element is the class name, and that there will be at
    # least one part of the module name
    name_parts = searchform.split('.')
    class_name = name_parts.pop()
    module_name = ".".join(name_parts)
    form_module = importlib.import_module(module_name)
    form_class = getattr(form_module, class_name, None)
    if not form_class:
        return {'avs_form': form, 'avs_redirect': redirect}

    def fix_labels(form):
        date_from = getattr(form.Meta, 'date_from', None)
        date_to = getattr(form.Meta, 'date_to', None)
        if date_from and date_from in form.fields:
            form.fields[date_from].label = "From " + form.fields[date_from].label  # noqa
        if date_to and date_to in form.fields:
            form.fields[date_to].label = "To " + form.fields[date_to].label

    if request.method == 'POST':
        form = form_class(request.POST)
        fix_labels(form)
        querystr = {}

        # copy over query string values that are not fields in the
        # advanced search form
        if len(request.GET.keys()) > 0:
            for key, value in request.GET.iteritems():
                skip = False
                for field in form.fields.keys():
                    if key.startswith(field):
                        skip = True
                if skip:
                    continue
                querystr[key] = value

        for field in form.fields.keys():
            fieldtype = type(form.fields.get(field))
            value = form.data.get(field)
            suffix = "__icontains"

            if models.ModelChoiceField == fieldtype:
                suffix = ""
            elif models.ModelMultipleChoiceField == fieldtype:
                suffix = "__in"
                value = ",".join(form.data.getlist(field))
            elif fields.DateField == fieldtype or fields.DateTimeField == fieldtype:  # noqa
                form_from = getattr(form.Meta, 'date_from', '')
                form_to = getattr(form.Meta, 'date_to', '')
                if form_from == field:
                    suffix = "__gte"
                elif form_to == field:
                    suffix = "__lte"
            elif fields.BooleanField == fieldtype:
                suffix = ""
                if value == "yes":
                    value = "True"
                elif value == "no":
                    value = "False"
                else:
                    value = ""

            key = "%s%s" % (field, suffix)
            if value.strip() == "":
                if key in querystr:
                    del querystr[key]
                continue

            querystr[key] = value

        vals = []
        if len(querystr.keys()) > 0:
            vals = ["%s=%s" % (urlquote_plus(field), urlquote_plus(val))
                    for field, val in querystr.iteritems()]
        redirect = "<script>document.body.style.display='none';window.location.href='%s?%s';</script>" \
            % (request.path, "&".join(vals))
    else:
        vals = {}
        form = form_class()
        if len(request.GET.keys()) > 0:
            for key, value in request.GET.iteritems():
                fieldname = key.split('__')[0]
                if fieldname in form.fields:
                    if type(form.fields.get(fieldname)) == fields.BooleanField:
                        if value == "True":
                            vals[fieldname] = "yes"
                        elif value == "False":
                            vals[fieldname] = "no"
                        else:
                            vals[fieldname] = "all"
                    else:
                        vals[fieldname] = value

            form = form_class(vals)
        fix_labels(form)

    return {'avs_form': form, 'avs_redirect': redirect}
