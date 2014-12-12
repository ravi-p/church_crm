from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    lst = map(request.path.startswith, urls.split())
    if any(lst):
        return "active"
    return ""

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
