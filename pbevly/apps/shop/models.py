# System libraries
import os

# Third-party libraries
# Django modules
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Django apps
from pbevly.apps.inventory.models import InventoryItem

# Current-app modules

# UPLOADS_STRING = "{}{}{}{}uploads".format(settings.BASE_DIR, os.sep, settings.STATIC_ROOT, os.sep)
"""

Models for the shop

"""


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    ORGANIZATION_OR_PERSON_CHOICES = [
        ('P', 'Person'),
        ('O', 'Organization'),
    ]
    organization_or_person = models.CharField(_("Organization or Person"), max_length=1,
                                              choices=ORGANIZATION_OR_PERSON_CHOICES,
                                              default='P')
    organization_name = models.CharField(_("Organization name"), max_length=40, default="")
    GENDER_CHOICES = [
        ('M', _("Male")),
        ('F', _("Female")),
    ]
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES)
    middle_initial = models.CharField(_("Middle initial"), max_length=1)
    phone_number = models.CharField(_("Phone"), max_length=10)
    address_line_1 = models.CharField(_("Address line 1"), max_length=40)
    address_line_2 = models.CharField(_("Address line 2"), max_length=40)
    address_line_3 = models.CharField(_("Address line 3"), max_length=40)
    address_line_4 = models.CharField(_("Address line 4"), max_length=40)
    city = models.CharField(_("City"), max_length=40)
    state = models.CharField(_("State"), max_length=40)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def full_name(self):
        if self.organization_or_person == 'O':
            return self.organization_name
        else:
            return "{} {}".format(self.user.first_name, self.user.last_name)

    def __str__(self):
        if self.organization_or_person == 'O':
            return self.organization_name
        else:
            return "{} {}".format(self.user.first_name, self.user.last_name)


class RefProductType(models.Model):
    parent_product_type_code = models.ForeignKey("self", null=True, blank=True,
                                                 on_delete=models.CASCADE,
                                                 verbose_name=_("Parent product type"))
    product_type_name = models.CharField(_("Product type name"), max_length=40)
    product_type_description = models.CharField(_("Product type description"), max_length=256)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return '{}'.format(self.product_type_name)


class Product(models.Model):
    product_type_code = models.ForeignKey(RefProductType, on_delete=models.CASCADE, verbose_name=_("Product type"))
    item_id = models.OneToOneField(InventoryItem, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Item"))
    product_name = models.CharField(_("Name"), max_length=40)
    product_price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2, default=0.)
    product_color = models.CharField(_("Color"), max_length=40)
    product_size = models.CharField(_("Size"), max_length=40)
    product_description = models.CharField(_("Description"), max_length=256)
    order_product_details = models.CharField(_("Other Details"), max_length=500)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return "{}".format(self.product_name)


class RefPaymentMethod(models.Model):
    payment_method_description = models.CharField(_("Payment method type"), max_length=256)

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment methods")

    def __str__(self):
        return self.payment_method_description


class CustomerPaymentMethod(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_("User"))
    payment_method_code = models.ForeignKey(RefPaymentMethod, on_delete=models.CASCADE,
                                            verbose_name=_("Payment method code"))
    credit_card_number = models.CharField(_("Credit/Debit card number"), max_length=16)
    payment_method_details = models.CharField(_("Details"), max_length=40)

    class Meta:
        verbose_name = _("Customer Payment Method")
        verbose_name_plural = _("Customer Payment Methods")

    def __str__(self):
        return "{} {} payment method {}".format(self.user_id.user.first_name, self.user_id.user.last_name, self.id)


class RefOrderStatusCode(models.Model):
    order_status_description = models.CharField(_("Order status code description"), max_length=256)

    class Meta:
        verbose_name = _("Order Status Code")
        verbose_name_plural = _("Order Status Codes")

    def __str__(self):
        return self.order_status_description


class Order(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_("User"))
    order_status_code = models.ForeignKey(RefOrderStatusCode, on_delete=models.CASCADE, verbose_name=_("Status code"))
    date_order_placed = models.DateTimeField(_("Date order placed"), auto_now_add=True)
    order_details = models.CharField(_("Order details"), max_length=256)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return "Order Number: {}\nOrdered By: {}\n".format(self.id, self.user_id.full_name())


class RefOrderItemStatusCode(models.Model):
    order_item_status_description = models.CharField(_("Status code description"), max_length=40)

    class Meta:
        verbose_name = _("Ordered Item Status Code")
        verbose_name_plural = _("Ordered Item Status Codes")

    def __str__(self):
        return self.order_item_status_description


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    order_item_status_code = models.ForeignKey(RefOrderItemStatusCode, on_delete=models.CASCADE,
                                               verbose_name=_("Status code"))
    order_item_quantity = models.IntegerField(_("Item quantity"))
    order_item_price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2, default=0.)
    other_order_item_details = models.CharField(_("Ordered item details"), max_length=256)
    RMA_number = models.CharField(_("Return label number"), max_length=50, blank=True)
    RMA_issued_by = models.CharField(_("Return label issued by"), max_length=40, blank=True)
    RMA_issued_date = models.DateTimeField(_("Return label issue date"), blank=True)

    class Meta:
        verbose_name = _("Ordered Item")
        verbose_name_plural = _("Ordered Items")

    def __str__(self):
        return "Order number: {}\n" \
               "Ordered by: {}\n" \
               "Product name: {}\n".format(self.order_id.id, self.order_id.user_id.full_name(),
                                           self.product_id.product_name)


class Shipment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("User"))
    shipment_tracking_number = models.CharField(_("Shipment tracking number"), max_length=255)
    shipment_date = models.DateTimeField(_("Date shipped"))
    order_shipment_details = models.CharField(_("Shipment details"), max_length=256)

    class Meta:
        verbose_name = _("Shipment")
        verbose_name_plural = _("Shipments")

    def __str__(self):
        return "Order number: {}\n" \
               "Ordered by: {}\n" \
               "Tracking Number: {}\n".format(self.order_id.id, self.order_id.user_id.full_name(),
                                              self.shipment_tracking_number)


class ShipmentItem(models.Model):
    shipment_id = models.ForeignKey(Shipment, on_delete=models.CASCADE, verbose_name=_("Shipment"))
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name=_("Order Item"))

    class Meta:
        verbose_name = _("Shipped Item")
        verbose_name_plural = _("Shipped Items")

    def __str__(self):
        return "Shipment number: {}\n" \
               "Product name: {}\n".format(self.shipment_id.id, self.order_item_id.product_id.product_name)


class RefInvoiceStatusCode(models.Model):
    invoice_status_description = models.CharField(_("Invoice status description"), max_length=256)

    class Meta:
        verbose_name = _("Invoice Status Code")
        verbose_name_plural = _("Invoice Status Codes")

    def __str__(self):
        return self.invoice_status_description


class Invoice(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"))
    invoice_status_code = models.ForeignKey(RefInvoiceStatusCode, on_delete=models.CASCADE, verbose_name=_("Status code"))
    invoice_date = models.DateTimeField(_("Invoice date"), auto_now_add=True)
    invoice_details = models.CharField(_("Invoice details"), max_length=256)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return "Invoice number: {}\n" \
               "Order Number: {}\n".format(self.id, self.order_id.id)


class Payment(models.Model):
    invoice_number = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name=_("Invoice"))
    payment_date = models.DateTimeField(_("Payment date"), auto_now_add=True)
    payment_amount = models.DecimalField(_("Amount"), max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return "Invoice: {}\n" \
               "Amount: {}\n".format(self.invoice_number.id, self.payment_amount)


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    product_image = models.ImageField(_("Image"), upload_to="uploads/",)
    image_name = models.CharField(_("Image title"), max_length=40)
    image_description = models.CharField(_("Description"), max_length=100)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return "{}".format(self.image_name)