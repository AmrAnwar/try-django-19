"""
{% load file_name(urlify)%}
"""
from urllib import quote_plus
from django import template

register = template.Library()


@register.filter
def urlify(value):
    """
    value|urlify
    :param value:
    :return quote_plus(value):
    """
    return quote_plus(value)
