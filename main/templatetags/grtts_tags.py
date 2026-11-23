import re

from django import template
from django.http import QueryDict
from django.template.defaultfilters import linebreaks
from django.utils.safestring import mark_safe

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


# A body that already contains block markup is HTML; anything else is typing.
_BLOCK_HTML = re.compile(r'<(p|div|table|h[1-6]|ul|ol|img|figure|section|br)[ >/]', re.I)


@register.filter
def rich_text(value):
    """Render a body that may be either pasted HTML or plain typed text.

    Newsletter campaigns are written in a plain admin textarea. Some are typed
    as prose, some are pasted in as prepared HTML. The template used to apply
    `|safe|linebreaks` to both, which wrapped pasted markup in stray <p> tags
    and scattered <br> between every block element.

    So: markup is passed through untouched, and typed prose still gets its
    paragraphs. Both are trusted, because only staff can write a campaign --
    exactly the trust `|safe` already assumed.
    """
    if not value:
        return ''
    text = str(value)
    if _BLOCK_HTML.search(text):
        return mark_safe(text)
    return linebreaks(text)
