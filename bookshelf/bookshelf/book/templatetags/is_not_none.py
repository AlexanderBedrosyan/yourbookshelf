from django import template

register = template.Library()

@register.filter
def is_not_none(value):
    return value is not None