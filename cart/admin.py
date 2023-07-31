from django.contrib import admin
from .models import Cart, CartItem
from products.api.models import Product
from .api.serializer import CartSerializer
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['uid']
    class Meta:
        model = Cart


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
