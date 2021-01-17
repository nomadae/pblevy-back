# System Libraries
# Third party libraries
# Django modules
from django.db import models
from django.utils.translation import gettext_lazy as _
# Django apps
# Current-app modules
"""

Models for Inventory control

"""


class Supplier(models.Model):
    supplier_name = models.CharField(_("Name"), max_length=40)
    supplier_email = models.CharField(_("Email"), max_length=40)
    supplier_phone = models.CharField(_("Phone"), max_length=10)
    supplier_cell_phone = models.CharField(_("Cellphone"), max_length=10)
    supplier_details = models.CharField(_("Details"), max_length=256)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.supplier_name


class Address(models.Model):
    line_1 = models.CharField(_("Line 1"), max_length=40)
    line_2 = models.CharField(_("Line 2"), max_length=40)
    line_3 = models.CharField(_("Line 3"), max_length=40)
    city = models.CharField(_("City"), max_length=40)
    postcode = models.CharField(_("PostCode"), max_length=40)
    state = models.CharField(_("State"), max_length=40)
    order_address_details = models.CharField(_("Other details"), max_length=256)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def full_address(self):
        return "{}\n" \
               "{}\n" \
               "{}\n".format(self.line_1, self.line_2, self.line_3)

    def __str__(self):
        return "{} {} {}".format(self.line_1, self.line_2, self. line_3)


class Brand(models.Model):
    brand_short_name = models.CharField(_("Short name"), max_length=40)
    brand_full_name = models.CharField(_("Full name"), max_length=100)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.brand_short_name


class RefItemCategory(models.Model):
    item_category_description = models.CharField(_("Category description"), max_length=256)

    class Meta:
        verbose_name = _("Item Category")
        verbose_name_plural = _("Item Categories")

    def __str__(self):
        return self.item_category_description


class InventoryItem(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"))
    category = models.ForeignKey(RefItemCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    item_description = models.CharField(_("Description"), max_length=256)
    average_monthly_usage = models.CharField(_("Average monthly usage"), max_length=40)
    reorder_level = models.CharField(_("Reorder level"), max_length=40)
    reorder_quantity = models.CharField(_("Reorder quantity"), max_length=40)
    other_item_details = models.CharField(_("Other Details"), max_length=256)

    class Meta:
        verbose_name = _("Inventory Item")
        verbose_name_plural = _("Inventory Items")

    def __str__(self):
        return self.item_description


class ItemSupplier(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_("Supplier"))
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name=_("Item"))
    value_supplied_to_date = models.CharField(_("Quantity supplied to date"), max_length=40)
    first_item_supplied_date = models.DateTimeField(_("First supply date"))
    last_item_supplied_date = models.DateTimeField(_("Last supply date"))
    delivery_lead_time = models.TimeField(_("Delivery time"))
    standard_price = models.DecimalField(_("Standard price"), max_digits=6, decimal_places=2)
    percentage_discount = models.DecimalField(_("Percentage discount"), max_digits=6, decimal_places=2)
    minimum_order_quantity = models.DecimalField(_("Minimum order quantity"), max_digits=6, decimal_places=2)
    maximum_order_quantity = models.DecimalField(_("Maximum order quantity"), max_digits=6, decimal_places=2)
    other_item_supplier_details = models.CharField(_("Other details"), max_length=256)

    class Meta:
        verbose_name = _("Item Supply")
        verbose_name_plural = _("Items Suppliers")

    def __str__(self):
        return "Supplier: {}\n" \
               "Item: {}\n".format(self.supplier.supplier_name, self.item.item_description)


class RefAddressType(models.Model):
    address_type_description = models.CharField(_("Address type description"), max_length=256)

    class Meta:
        verbose_name = _("Address type")
        verbose_name_plural = _("Address types")

    def __str__(self):
        return "{}".format(self.address_type_description)


class SupplierAddress(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_("Supplier"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name=_("Address"))
    address_type = models.ForeignKey(RefAddressType, on_delete=models.CASCADE, verbose_name=_("Address type"))
    date_address_from = models.DateTimeField(_("Departure date"))
    date_address_to = models.DateTimeField(_("Arrival date"))

    class Meta:
        verbose_name = _("Supplier address")
        verbose_name_plural = _("Supplier addresses")

    def __str__(self):
        return "Supplier: {}\n" \
               "Address from departure: {}\n" \
               "Departure date: {}\n" \
               "Arrival date: {}\n".format(self.supplier, self.address.full_address(), self.date_address_to,
                                           self.date_address_from)


class ItemStockLevel(models.Model):
    stock_taking_dates = models.DateTimeField(_("Stock taking date"), primary_key=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name=_("Item"))
    quantity_in_stock = models.IntegerField(_("Quantity in stock"), default=0)

    class Meta:
        verbose_name = _("Item stock level")
        verbose_name_plural = _("Item stock levels")

    def __str__(self):
        return "Last taken: {}\n" \
               "In stock: {}\n".format(self.stock_taking_dates, self.quantity_in_stock)