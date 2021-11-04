from django import template


register = template.Library()


@register.filter
def round_number(number:float, decimal_places:int=0):
    return str(round(number, decimal_places)).replace(',', '.')