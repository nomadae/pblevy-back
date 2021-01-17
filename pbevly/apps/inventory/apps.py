from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = "pbevly.apps.inventory"
    verbose_name = _("Inventory")

    def ready(self):
        from . import signals