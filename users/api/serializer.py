from users.models import User, UserBilling
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
import stripe
import json
import os
from rest_framework_simplejwt.tokens import RefreshToken

stripe.api_key = os.getenv('SK')

class UserBillingSerializer(ModelSerializer):
    class Meta:
        model = UserBilling
        fields = '__all__'

class UserSerializer(ModelSerializer):
    addresses = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'stripe', 'cards', 'addresses' , 'id','password', 'is_active','subscription']
    def get_cards(self, request):
        stripeData = stripe.PaymentMethod.list(
            customer=request.stripe,
            type="card",
            limit=100
        )
        print(len(stripeData.data))
        print(len(stripeData.data))
        print(len(stripeData.data))
        cards = [None for card in stripeData.data]
        i = 0
        customer = stripe.Customer.retrieve(request.stripe)
        customer['invoice_settings']['default_payment_method']
        for card in stripeData.data:
            p = {}
            p['id'] = card.id
            p['brand'] = card.card.brand
            p['last4'] = card.card.last4
            if customer['invoice_settings']['default_payment_method'] == p['id']:
                p['default'] =  True
            else:
                p['default'] =  False
            p['exp'] = {}
            p['exp']['month'] = card.card.exp_month
            p['exp']['year'] = card.card.exp_year
            p['icon'] ='https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-'+ p['brand'] + '.svg'
            cards[i] = p
            i = i+1
        return cards
    def get_addresses(self, request):
        info = UserBilling.objects.filter(user_id__email=request.email)
        addresses = UserBillingSerializer(info, many=True)
        return addresses.data





class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'stripe']
    def create(self, validated_data):
        customer = self.stripe_create(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.stripe = customer
        instance.save()
        return instance

    def stripe_create(self, validated_data):
        customer = stripe.Customer.create(
            email=validated_data['email'],
            name=validated_data['first_name'] + " " + validated_data['last_name']
        )
        return customer.id



class UserRegisterSerializer_Subscription(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'stripe']
    def create(self, validated_data):
        customer = self.stripe_create(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.stripe = customer
        instance.save()
        return instance
    def stripe_create(self, validated_data):
        customer = stripe.Customer.create(
            email=validated_data['email'],
            name=validated_data['first_name'] + " " + validated_data['last_name']
        )
        return customer.id
