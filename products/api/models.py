from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from products.api.serializers import ProductSerializer, TagsSerializer, ProductVariation
from products.models import Product, ProductTag
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters

class ProductAPIView(ViewSet):
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    @swagger_auto_schema(operation_description="List all Products", operation_id="productsList")
    def list(self, request):
        tags = request.query_params.get('tags', None)
        max_price = request.query_params.get('max_price', None)
        min_price = request.query_params.get('min_price', None)
        print(tags)
        if tags:
            tags = tags.split(',')
            objects = Product.objects.filter(tags__id__in=tags, published=True).distinct()
        else:
            objects = Product.objects.filter(published=True)
        serializer = ProductSerializer(objects, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    @swagger_auto_schema(operation_description="Find a product with a slug", responses={404: 'slug not found'}, operation_id="productsFind")
    def retrieve(self, request, slug: str):
        queryset = Product.objects.filter(slug=slug, published=True)
        if len(queryset) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail":"product not found"})
        else:
            serializer = ProductSerializer(queryset[0])
            return Response(status=status.HTTP_200_OK, data=serializer.data)



class TagAPIView(ViewSet):
    @swagger_auto_schema(operation_description="List all Product Tags", operation_id="tagLists")
    def list(self, request):
        array = []
        serializer = TagsSerializer(ProductTag.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)