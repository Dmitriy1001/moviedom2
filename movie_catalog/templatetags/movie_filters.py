from math import ceil

from django import template
from django.db.models import Count

register = template.Library()


@register.filter
def round_number(number:(int,float), decimal_places:int=0):
    if isinstance(number, (int, float)):
        return str(round(number, decimal_places)).replace(',', '.')
    return 0


@register.filter
def text_slice(text, text_range):
    text = text.split()
    start, end = text_range.split(',')
    if end != 'full':
        return ' '.join(text[int(start):int(end)])
    return ' '.join(text[int(start):])


@register.filter
def split_text(text, split_by:str=' '):
    return text.split(split_by)


@register.filter
def isnumber(value):
    return type(value) in (int, float)


@register.filter
def format_youtube_url(url:str):
    '''formats youtube link for iframe tag'''
    return url.replace('watch?v=', 'embed/')


@register.filter
def comments_count(none_parent_comments):
    return (
            len(none_parent_comments) +
            none_parent_comments.aggregate(Count('replies'))['replies__count']
    )


@register.filter
def change_number_sign(number: (int, float)):
    number = 0 if number is None else number
    return -number if number > 0 else abs(number)


@register.filter
def convert_to(value, convert_type):
    return convert_type(value)
