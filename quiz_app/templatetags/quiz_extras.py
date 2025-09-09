from django import template

register = template.Library()

@register.filter
def get_item(list_obj, index):
    try:
        return list_obj[index]
    except:
        return None

@register.filter
def get_option(question, option_number):
    return getattr(question, f'option{option_number}', '')