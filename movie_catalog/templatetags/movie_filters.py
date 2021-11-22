from django import template


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