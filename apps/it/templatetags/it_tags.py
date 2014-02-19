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
