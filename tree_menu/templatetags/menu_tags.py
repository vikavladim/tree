from django import template
from ..models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info

    try:
        menu = Menu.objects.prefetch_related(
            'items__children__children__children'
        ).get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    def get_visible_items(items, current_url, parent=None, level=0):
        visible_items = []
        for item in items.filter(parent=parent).order_by('order'):
            item_url = item.get_url()
            is_active = current_url.startswith(item_url)
            show_item = (level == 0) or current_url.startswith(
                item.parent.get_url() if item.parent else ''
            )

            if show_item:
                visible_items.append({
                    'item': item,
                    'url': item_url,
                    'is_active': is_active,
                    'level': level,
                    'children': get_visible_items(items, current_url, item, level + 1)
                })

        return visible_items

    menu_tree = get_visible_items(menu.items.all(), current_url)
    return {'menu_tree': menu_tree}
