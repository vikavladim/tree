from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    verbose_name = models.CharField(_('verbose name'), max_length=100)

    class Meta:
        app_label = 'tree_menu'
        db_table = 'tree_menu_menu'
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __str__(self):
        return self.verbose_name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name=_('menu'),
        related_name='items'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=_('parent item'),
        related_name='children',
        null=True,
        blank=True
    )
    verbose_name = models.CharField(_('verbose name'), max_length=100)
    url = models.CharField(
        _('link'),
        max_length=255,
        blank=True,
        help_text=_('URL or named URL pattern')
    )
    named_url = models.CharField(
        _('named URL'),
        max_length=100,
        blank=True,
        help_text=_('Named URL pattern (e.g., "products:index")')
    )
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'tree_menu'
        db_table = 'tree_menu_menuitem'
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
        ordering = ['order']

    def __str__(self):
        return self.verbose_name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.named_url
        return self.url or '#'

    def is_active(self, current_url):
        return current_url == self.get_url()

    def save(self, *args, **kwargs):
        if not self.url and not self.named_url:
            self.url = f'/{self.menu.name}/{self.slug}/'
        super().save(*args, **kwargs)

    @property
    def is_expanded(self, current_url):
        return current_url.startswith(self.get_url())

    @property
    def slug(self):
        return (self.verbose_name.lower()
                .replace(' ', '-')
                .replace('/', '-'))
