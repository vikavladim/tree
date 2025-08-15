from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from django.core.management import call_command
        call_command('refresh_urls')

admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)