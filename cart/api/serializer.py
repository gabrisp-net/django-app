from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.api.serializers import ProductSerializer, ProductVariationSerializer
from cart.models import Cart, CartItem
from products.models import Product, ProductVariation
import numpy as np
import random

class CartItemSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    variation = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['quantity', 'product', 'variation','id']
    def get_product(self, pk):
        serializer = ProductSerializer(Product.objects.get(id=pk.product_id.id))
        return serializer.data
    def get_variation(self, pk):
        if pk.variation_id:
            variation = ProductVariationSerializer(ProductVariation.objects.get(id=pk.variation_id.id))
            return variation.data
        else:
            return None




class CartSerializer(ModelSerializer):
    products = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    lookup_field = ['uid']
    class Meta:
        model = Cart
        fields = ['uid', 'total', 'quantity', 'products', 'recommendations']
    def get_products(self, pk):
        serializer = CartItemSerializer(CartItem.objects.filter(cart_id=pk.pk), many=True)
        return serializer.data
    def get_total(self, pk):
        price = 0
        items = CartItem.objects.filter(cart_id=pk.pk)
        array_qty = [item.quantity for item in items]
        for i in items:
            if i.variation_id == None:
                price = (i.quantity * i.product_id.price) + price
            else:
                price = (i.quantity * i.variation_id.price) + price
        price = price
        return float(price)
    def get_quantity(self, pk):
        quantity = 0
        items = CartItem.objects.filter(cart_id=pk.pk)
        array = [item.quantity for item in items]
        for i in array:
            quantity = quantity + i
        return quantity
    def get_recommendations(self, pk):
        items = CartItem.objects.filter(cart_id=pk.pk)
        all = ProductSerializer(Product.objects.filter(published=True), many=True).data
        i = 0
        if len(items) > 0:
            while i < len(items):
                for item in all:
                    if item['id'] == items[i].product_id.id:
                        all.remove(item)
                i = i + 1
        print(len(all))
        random.shuffle(all)
        return all[slice(1)]

