from django import template

register = template.Library()


@register.filter
def random_results(qs, number):
    return qs.order_by('?')[:number]
