from django import template

register = template.Library

@register.simple_tag
def display_name(user):
    first_name=user.userprofile.first_name
    if first_name:
        return first_name
