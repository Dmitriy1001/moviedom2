import re

from django import template


register = template.Library()


@register.filter
def round_number(number:float, decimal_places:int=0):
    if isinstance(number, (int, float)):
        return str(round(number, decimal_places)).replace(',', '.')
    return 0


@register.filter
def first_words(text, words_number:int):
    return re.sub(
        r'.+([,\.:-;])$',
        lambda chars: chars[0].replace(chars[1], ''),
        ' '.join(text.split()[:words_number]),
    ) + '...'


@register.filter
def isnumber(value):
    return type(value) in (int, float)