from nanoid import generate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CartSerializer,CartItemSerializer
from products.models import Product, ProductVariation
from cart.models import Cart, CartItem
from products.api.serializers import ProductSerializer


class CartAPIView(ViewSet):
    lookup_field = 'uid'
    @swagger_auto_schema(deprecated=True, auto_schema=None)
    def list(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": {"code": 404, "message": "Cart not finded."}})

    @swagger_auto_schema(operation_description="Find a Cart with its Slug", responses={404: 'slug not found'},
                         operation_id="cartFind")
    def retrieve(self, request, uid: str):
        queryset = Cart.objects.get(uid=uid)
        serializer = CartSerializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(operation_description="Create a Cart", operation_id="cartCreate")
    def create(self, request):
        urlhash = generate()
        while Cart.objects.filter(uid=urlhash).exists():
            urlhash = generate()
        cart = Cart.objects.create(uid=urlhash)
        cart.save()
        queryset = Cart.objects.get(uid=urlhash)
        data = CartSerializer(queryset)
        return Response(status=status.HTTP_200_OK, data=data.data)


class CartAddItemAPIView(APIView):
    @swagger_auto_schema(operation_description="Add product to the cart",operation_id="cartAddProduct", responses={404: 'cart/product not found'})
    def post(self, request, cart, product):
       findedProduct = Product.objects.get(slug=product)
       findedCart = Cart.objects.get(uid=cart)
       if request.GET.get('i'):
           findedVariation = ProductVariation.objects.get(id=int(request.GET.get('i')))
           cartItem = CartItem.objects.filter(product_id=findedProduct.id, cart_id=findedCart.id, variation_id=findedVariation)
       else:
        cartItem = CartItem.objects.filter(product_id=findedProduct.id, cart_id=findedCart.id, variation_id=None)
       if len(cartItem)>0:
           cartItem[0].quantity = cartItem[0].quantity + 1
           cartItem[0].save()
       else:
           if request.GET.get('i'):
            findedVariation = ProductVariation.objects.get(id=int(request.GET.get('i')))
            create = CartItem.objects.create(product_id=findedProduct, cart_id=findedCart, quantity=1, variation_id=findedVariation)
           else:
               create = CartItem.objects.create(product_id=findedProduct, cart_id=findedCart, quantity=1)
           create.save()
       queryset = Cart.objects.get(uid=cart)
       serializer = CartSerializer(queryset)
       return Response(status=status.HTTP_200_OK, data=serializer.data)


class CartRemoveItemAPIView(APIView):
    @swagger_auto_schema(operation_description="Remove product from the cart", operation_id="cartRemoveProduct", responses={404: 'cart/product not finded'})
    def post(self, request, cart, product):
       findedProduct = Product.objects.get(slug=product)
       findedCart = Cart.objects.get(uid=cart)
       if request.GET.get('i'):
           findedVariation = ProductVariation.objects.get(id=int(request.GET.get('i')))
           product = CartItem.objects.filter(product_id_id=findedProduct.id, cart_id_id=findedCart.id, variation_id_id=findedVariation.id)
       else:
           product = CartItem.objects.filter(product_id_id=findedProduct.id, cart_id_id=findedCart.id)
       if product:
            if product[0].quantity == 1:
                product[0].delete()
            else:
                product[0].quantity = product[0].quantity - 1
                product[0].save()
            queryset = Cart.objects.get(uid=cart)
            serializer = CartSerializer(queryset)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
       else:
           return Response(status=status.HTTP_404_NOT_FOUND, data={"error":{"code": 404, "message": "Product not finded."}})

class CartIsIn(APIView):
    def get(self,request, cart, product):
        findedProduct = Product.objects.get(slug=product)
        findedCart = Cart.objects.get(uid=cart)
        product = CartItem.objects.filter(product_id_id=findedProduct.id, cart_id_id=findedCart.id)
        if product:
            data = CartItemSerializer(product, many=True)
            return Response(status=status.HTTP_200_OK, data=data.data[0])
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={{"Product not in cart."}})

class DeleteCart(APIView):
    def post(self, request, cart):
        findedCart = Cart.objects.get(uid=cart)
        findedItems = CartItem.objects.filter(cart_id_id=findedCart.id)
        findedItems.delete()
        return Response(status=status.HTTP_200_OK, data="ok" )