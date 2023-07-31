import random
from rest_framework.serializers import ModelSerializer
from products.models import Product, ProductImage, ProductDowload, ProductTag, ProductVariation, ProductSpecs
from rest_framework import serializers
import blurhash

class ProductSpecsSerializer(ModelSerializer):
    class Meta:
        model = ProductSpecs
        fields = ['key','value']
class ProductImageSerializer(ModelSerializer):
    hash = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = ['url', 'alt', 'hash', 'type']
    def get_hash(self, pk):
        #hash = blurhash.encode(pk.url, x_components=4, y_components=3)
        return "hash"

class ProductVariationSerializer(ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['name', 'price', 'id','stock']
class ProductRecommendationSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()
    lookup_field = 'slug'
    class Meta:
        model = Product
        fields = ['id','title', 'price', 'slug', 'images']
    def get_images(self, pk):
        serializer = ProductImageSerializer(ProductImage.objects.filter(product_id=pk.pk), many=True)
        return serializer.data

class ProductSerializer(ModelSerializer):
    images = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    variations = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()
    lookup_field = 'slug'
    class Meta:
        model = Product
        fields = ['id','title', 'price', 'slug', 'color', 'images', 'tags','description','line', 'recommendations', "comingsoon", "date", "variations",'stock', 'specs']
    def get_images(self, pk):
        serializer = ProductImageSerializer(ProductImage.objects.filter(product_id=pk.pk), many=True)
        return serializer.data
    def get_variations(self, pk):
        serializer = ProductVariationSerializer(ProductVariation.objects.filter(product=pk.pk), many=True)
        return serializer.data
    def get_specs(self, pk):
        serializer = ProductSpecsSerializer(ProductSpecs.objects.filter(product=pk.pk), many=True)
        return serializer.data
    def get_recommendations(self, pk):
        itemPage = Product.objects.get(id=pk.pk)
        all = ProductRecommendationSerializer(Product.objects.filter(published=True), many=True)
        random.shuffle(all.data)
        for item in all.data:
            if item['id'] == itemPage.id:
              all.data.remove(item)
        return all.data[slice(5)]


class ProductDownloadSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = ProductDowload
        fields = ['url', 'left' ,'uid','product']
    def get_url(self, pk):
        return "http://127.0.0.1:8000/api/download/" + pk.uid
    def get_product(self, pk):
        product = ProductSerializer(Product.objects.get(id=pk.product_id.id))
        return product.data



class TagsSerializer(ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id','name']
