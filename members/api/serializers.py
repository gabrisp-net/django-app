from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from products.api.serializers import ProductSerializer
from products.models import Product
from members.models import VideoMembership, ItemMembership, ProductMembership, Membership
import stripe
import os

stripe.api_key = os.getenv('SK')

#Locked
class Locked_ProductMembers(ModelSerializer):
    product = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = ProductMembership
        fields = ['type','product', 'type','preview']
    def get_product(self, pk):
        product = ProductSerializer(Product.objects.get(id=pk.product_id.id))
        return product.data
    def get_type(self, pk):
        return 'product'

class Locked_ItemMembers(ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = ItemMembership
        fields = ['type','title', 'text','slug', 'preview']
    def get_type(self, pk):
        return 'item'


class Locked_VideoMembers(ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = VideoMembership
        fields = ['type','title', 'text', 'slug', 'preview']
    def get_type(self, pk):
        return 'video'

#Unlocked
class Unlocked_ProductMembers(ModelSerializer):
    product = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = ProductMembership
        fields = ['type','product', 'type','preview']
    def get_product(self, pk):
        product = ProductSerializer(Product.objects.get(id=pk.product_id.id))
        return product.data
    def get_type(self, pk):
        return 'product'

class Unlocked_ItemMembers(ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = ItemMembership
        fields = ['type','title', 'text','slug', 'preview','file']
    def get_type(self, pk):
        return 'item'


class Unlocked_VideoMembers(ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = VideoMembership
        fields = ['type','title', 'text', 'slug', 'preview','url']
    def get_type(self, pk):
        return 'video'


class OneMembershipSerializer(ModelSerializer):
    stripe = serializers.SerializerMethodField()
    class Meta:
        model = Membership
        fields = ['id','title', 'billing','description','price','stripe']
    def get_stripe(self, request,):
        data = stripe.Price().retrieve(id=request.id_stripe, expand=['currency_options'])
        return data



