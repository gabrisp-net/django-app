import stripe
from rest_framework import serializers
from orders.models import Order
from products.models import ProductDowload, Product
from products.api.serializers import ProductDownloadSerializer

class OrderSerializer(serializers.ModelSerializer):
    downloads = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    class Meta:
        model = Order
        lookup_fields = ['uid']
        fields = ['uid', 'cart', 'stripe', 'downloads','date', 'billing_address', 'payment_method']
    def get_downloads(self, pk):
        downloads = ProductDownloadSerializer(ProductDowload.objects.filter(order=pk.pk), many=True)
        return downloads.data
    def get_payment_method(self, pk):
        payment = {}
        if pk.stripe['method'] == 'paypal':
            payment['type'] = 'paypal'
            payment['icon'] = 'https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-paypal.png'
            return payment
        method = stripe.PaymentMethod.retrieve(pk.stripe['payment_method'])
        if method['card']['wallet'] is not None :
            payment['type'] = 'wallet'
            payment['icon'] = ['https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-'+ method['card']['brand'] + '.svg', 'https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-'+ method['card']['wallet']['type'] + '.png']
            payment['exp'] = {}
            payment['exp']['month'] =  method['card']['exp_month']
            payment['exp']['year'] = method['card']['exp_year']
            payment['last4'] = method['card']['last4']
            payment['brand'] = [method['card']['wallet']['type'], method['card']['brand']]
        else:
            payment['type'] = 'card'
            payment['icon'] = 'https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-'+ method['card']['brand'] + '.svg'
            payment['exp'] = {}
            payment['exp']['month'] =  method['card']['exp_month']
            payment['exp']['year'] = method['card']['exp_year']
            payment['last4'] = method['card']['last4']
            payment['brand'] =  method['card']['brand']
        return payment


