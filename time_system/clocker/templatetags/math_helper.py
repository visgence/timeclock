from django import template
from decimal import *
register = template.Library()

myothercontext = Context(prec=4)
#getcontext().prec = 3
@register.filter
def to_hour(value):
    setcontext(myothercontext)
    return Decimal(value) / 3600
