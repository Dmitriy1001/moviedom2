from django import template


register = template.Library()


@register.filter
def round_number(number:float, decimal_places:int=0):
    if isinstance(number, (int, float)):
        return str(round(number, decimal_places)).replace(',', '.')
    return 0