from django import template
register = template.Library()
def to_hour(value):
    return float(value) / 3600.
register.filter('to_hour', to_hour)
