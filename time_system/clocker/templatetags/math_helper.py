from django import template
from decimal import *
register = template.Library()

getcontext().prec = 3 
@register.filter
def to_hour(value):
    return Decimal(value) / 3600
