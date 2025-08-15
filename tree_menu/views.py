from django.shortcuts import render
from tree_menu.models import Menu

def index(request):
    main_menu, created = Menu.objects.get_or_create(
        name='main_menu',
        defaults={'verbose_name': 'Main Menu'}
    )
    return render(request, 'tree_menu/index.html', {'menu': main_menu})