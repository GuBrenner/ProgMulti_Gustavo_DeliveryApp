from django import template

register = template.Library()

@register.filter
def sum(items, attr):
    return sum(getattr(i, attr) for i in items)