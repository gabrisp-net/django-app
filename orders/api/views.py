import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from nanoid import generate
from orders.models import Order
from products.models import ProductDowload
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.api.serializers import OrderSerializer
from products.models import Product
import stripe
import os
from django.conf import settings

from users.api.serializer import UserSerializer

stripe.api_key = os.getenv('SK')


class OrderView(APIView):
    def post(self, request):
       print("request.POST")
       cart = request.data['cart']
       print(cart['products'])
       print("request.POST")
       if request.data['stripe']['method'] == "paypal":
           pi = {}
           info = requests.get('http://127.0.0.1:8000/api/paypal/order/?id='+ request.data['payment_intent'])
           pi['status'] =info.json()['status']
       else:
           pi = stripe.PaymentIntent.retrieve(
               request.data['payment_intent']
           )
       if pi['status'] == "succeeded" or pi['status'] == "APPROVED":
           if request.user.is_authenticated:
               urlhash = generate("0123456789", 10)
               while Order.objects.filter(uid=urlhash).exists():
                   urlhash = generate()
               order = Order.objects.create(
                   uid=urlhash,
                   cart=request.data['cart'],
                   stripe=request.data['stripe'],
                   payment_intent=request.data['payment_intent'],
                   billing_address=request.data['billing_address'],
                   user=request.user
               )
               order.save()
               count = 0
               for item in cart['products']:
                   product_id = item['product']
                   product = Product.objects.get(id=product_id['id'])
                   print(product)
                   product.stock = product.stock - item['quantity']
                   product.save()
                   download =ProductDowload.objects.create(order=order, product_id=product, uid=(order.uid + "-file" + str(count)), left=item['quantity']*3)
                   download.save()
                   count=count+1
               order = OrderSerializer(Order.objects.get(id=order.id))
               userSerialized = UserSerializer(request.user)
               print(userSerialized.data)
               print(order.data)

               subject = 'Order #' + order.data['uid'] + ' confirmed!'
               to = [userSerialized.data['email'], ]
               from_ = f'Gabrisp <{settings.EMAIL_HOST_USER}>'
               content = render_to_string('emails/orderConfirmation.html', {"order":order.data, "user": userSerialized.data})
               send_mail(subject, "", from_, to, html_message=content, fail_silently=True)
               return Response(status=status.HTTP_200_OK, data=order.data)
           else:
               return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "not authorized"})
       else:
           return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "payment intent not succeed."})


class getOrderView(APIView):
    def get(self, request, id):
        orderData = Order.objects.filter(uid=id)
        print(orderData)
        if len(orderData) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail":"order not found"})
        elif orderData[0].user == request.user:
            order = OrderSerializer(orderData[0])
            return Response(status=status.HTTP_200_OK, data=order.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail":"order not found"})

class getOrders(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            orderData = Order.objects.filter(user=request.user)
            order = OrderSerializer(orderData, many=True)
            return Response(status=status.HTTP_200_OK, data=order.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail":"Not authenticated."})

