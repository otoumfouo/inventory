from django import template
from django.db.models import Sum

register = template.Library()

@register.filter(name='placeholder')
def placeholder(field, text):
   return field.as_widget(attrs={"placeholder":text})\

@register.filter(name='id')
def id(field, text):
   return field.as_widget(attrs={"id":text})

@register.filter(name='sum')
def sum(field, sumfield):
   nbre = field.aggregate(Sum(sumfield)).get(sumfield+'__sum')
   #return nbre if nbre =='None' else 0
   return field.aggregate(Sum(sumfield)).get(sumfield+'__sum')