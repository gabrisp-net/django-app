import string
from random import random

from django.db import models
from products.models import Product, ProductVariation


class Cart(models.Model):
    uid = models.CharField(max_length=6, null=True, blank=True, unique=True)
    #user = models.ForeignKey(User,  blank=True, null=True, on_delete=models.CASCADE)
    def items(self):
        items = CartItem.objects.filter(product_id_id=self.id)
        return items


class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    product_id = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    variation_id = models.ForeignKey(ProductVariation, blank=True, null=True, on_delete=models.CASCADE)
    cart_id = models.ForeignKey('Cart', default=None, on_delete=models.CASCADE)
    def product(self):
        product = Product.objects.get(pk=self.product_id)
        return product
