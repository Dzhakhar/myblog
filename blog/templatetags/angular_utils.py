from django import template


register = template.Library()


def interpolate(value):
    return "{{ %s }}" % value


register.filter('interpolate', interpolate)