from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import path, clear_url_caches
from django.apps import apps
from django.core.exceptions import AppRegistryNotReady
from importlib import reload, import_module
import sys


def generate_urlpatterns():
    try:
        MenuItem = apps.get_model('tree_menu', 'MenuItem')
        urlpatterns = []

        for item in MenuItem.objects.all():
            path_str = item.url.lstrip('/') if item.url else f"{item.menu.name}/{item.slug}/"
            urlpatterns.append(
                path(path_str, generic_view, name=f"menu_{item.id}")
            )

        return urlpatterns
    except AppRegistryNotReady:
        return []


def generic_view(request):
    from django.shortcuts import render
    return render(request, 'tree_menu/generic_page.html', {
        'request': request
    })


@receiver(post_save, sender='tree_menu.MenuItem')
def update_urls(sender, instance, **kwargs):
    try:
        urls_module = import_module('tree_menu.urls')
        clear_url_caches()

        if 'tree_menu.urls' in sys.modules:
            reload(sys.modules['tree_menu.urls'])
    except ModuleNotFoundError:
        pass