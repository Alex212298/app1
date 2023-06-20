from django import template

register = template.Library()

ban_list = ["max's", 'for', 'title']

@register.filter(name='censor')
def censor(value):
    text = value.split()
    for i in text:
        if i in ban_list:
            value = value.replace(i, '***')
    return value



