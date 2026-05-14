from django import template

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(lst, i):
    try:
        return lst[i]
    except (IndexError, TypeError):
        return None

@register.simple_tag
def sum_workload(workload):
    return sum(v['total'] for v in workload.values())
