from django import template

from blog.models import Favourites


register = template.Library()


def interpolate(value):
    return "{{ %s }}" % value

def is_liked(user, post_id):
    return Favourites.objects.filter(
        user=user, postt__id=post_id, active=True).count() != 0

register.filter('interpolate', interpolate)
register.filter('is_liked', is_liked)
