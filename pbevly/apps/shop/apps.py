from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    name = "pbevly.apps.shop"
    verbose_name = _("Shop")

    def ready(self):
        from . import signals
