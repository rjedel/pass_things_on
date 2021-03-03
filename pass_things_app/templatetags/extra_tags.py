from django import template

from pass_things_app.models import Institution

register = template.Library()


@register.filter
def categories_str(queryset):
    return ', '.join(cat.name for cat in queryset.order_by('name')[:5])


@register.filter
def display_description(obj_pk):
    return Institution.objects.get(pk=obj_pk).description
