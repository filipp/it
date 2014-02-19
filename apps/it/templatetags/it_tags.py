# -*- coding: utf-8 -*-

from django import template
from django.utils import safestring, timezone
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def markdown(text):
    import markdown
    result = markdown.markdown(text)
    return safestring.mark_safe(result)

@register.simple_tag
def new_issue_count(request):
    return safestring.mark_safe('14')

@register.simple_tag
def new_asset_count(request):
    return safestring.mark_safe('9')

@register.simple_tag
def new_docs_count(request):
    return safestring.mark_safe('6')
