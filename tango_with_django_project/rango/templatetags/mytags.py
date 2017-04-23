from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/side_bar.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act-category': cat}
