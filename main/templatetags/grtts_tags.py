from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def query_replace(context, **kwargs):
    """Return the current query string with the given parameters replaced.

    Used by the pagers: `?{% query_replace page=3 %}` keeps whatever search or
    filter is active and changes only the page. An empty value drops the
    parameter.
    """
    request = context.get('request')
    params = request.GET.copy() if request is not None else QueryDict(mutable=True)

    for key, value in kwargs.items():
        if value in (None, ''):
            params.pop(key, None)
        else:
            params[key] = value

    return params.urlencode()
