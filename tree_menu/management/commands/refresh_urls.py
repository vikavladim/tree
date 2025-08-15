from django.core.management.base import BaseCommand
from django.urls import clear_url_caches
from importlib import reload, import_module
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Refresh URL patterns'

    def handle(self, *args, **options):
        try:
            urls_module = import_module('tree_menu.urls')
        except ModuleNotFoundError:
            self.stdout.write(self.style.ERROR('tree_menu.urls module not found'))
            return

        clear_url_caches()

        if 'tree_menu.urls' in sys.modules:
            reload(sys.modules['tree_menu.urls'])

        self.stdout.write(self.style.SUCCESS('URL patterns refreshed successfully'))