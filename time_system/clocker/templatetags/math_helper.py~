from django import template
register = template.Library()
register.filter('to_hour', to_hour)
def to_hour(value):
    return float(value) / 3600.
