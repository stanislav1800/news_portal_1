from django import template
import re

register = template.Library()

_TAGS = [('редис','р****'), ('Редиска','Р******')]

@register.filter(name='length')
def currency(value):

   return f'{len(value)} '

@register.filter(name='censor')
def currency(value):
   if type(value)==str:
      for pattern, repl in _TAGS:
        value = re.sub(pattern, repl, value)
   return value 

@register.filter(name='post_id')
def currency(value):
   return f'/news/{value}'