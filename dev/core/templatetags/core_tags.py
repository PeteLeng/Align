from django import template

register = template.Library()

@register.filter
def show_visibility(value):
    return "public" if value else "private"
