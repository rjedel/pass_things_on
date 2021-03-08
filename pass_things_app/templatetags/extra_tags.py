from django import template

register = template.Library()


@register.filter
def categories_str(queryset):
    return ', '.join(cat.name for cat in queryset.order_by('name')[:5])
