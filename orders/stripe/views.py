import base64

import requests

from rest_framework import status
from rest_framework.views import APIView
import stripe
import os
from rest_framework.response import Response
import json
from cart.api.serializer import CartSerializer, CartItemSerializer
from cart.models import CartItem, Cart
stripe.api_key = os.getenv('SK')


class PaymentMethodView(APIView):
    def get(self, request, id):
        data = stripe.PaymentMethod.retrieve(id)
        return Response(status=status.HTTP_200_OK, data=data)

class PaymentIntentView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.GET.get("price"):
                if request.GET.get('save_card') == "true":
                    data = stripe.PaymentIntent.create(
                        amount=request.GET.get("price"),
                        currency="eur",
                        customer=request.user.stripe,
                        setup_future_usage='off_session',
                    )
                elif request.GET.get('pi'):
                    data = stripe.PaymentIntent.create(
                        amount=request.GET.get("price"),
                        currency="eur",
                        customer=request.user.stripe,
                        payment_method = request.GET.get('pi'),
                    )
                else:
                    data = stripe.PaymentIntent.create(
                        amount=request.GET.get("price"),
                        currency="eur",
                        customer=request.user.stripe,
                        payment_method_types=['card', 'klarna']
                    )
                return Response(status=status.HTTP_200_OK, data={"client_secret": data["client_secret"]})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": {"message":"no price submitted"}})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": {"message": "not authenticated"}})


class CardViews(APIView):
    def get(self, request, cards=None):
        counter = 0
        if request.user.is_authenticated:
            data = stripe.PaymentMethod.list(
                    customer=request.user.stripe,
                    type="card",
            )
            print(data)
            return Response(status=status.HTTP_200_OK, data=data.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": {"message": "not authenticated"}})



class CustomerView(APIView):
    def get(self, request, cards=None):
        if request.user.is_authenticated:
            data = stripe.Customer.retrieve(request.user.stripe)
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": {"message": "not authenticated"}})


        #Paypal

def PaypalToken():
            client_ID = "Aa-WsRJvODq4xH4iztuzJu-TXBNYB9pWNjn9Yyh1IwG10ptSweT0-gcGqDXfXdjEIk4olhHr2bVC12Se"
            client_Secret = "EB-GVd6nrC44UVPloTpOhlhBsvAtp9fSKGzPCc42CFkzCn_7e8ud_E-wSebvxh3XusXEhtfMkCOgI4h0"
            url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
            data = {
                "client_id": client_ID,
                "client_secret": client_Secret,
                "grant_type": "client_credentials"
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {0}".format(
                    base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())
            }

            token = requests.post(url, data, headers=headers)
            print(token)
            return token

def make_paypal_payment(amount, tax, currency, return_url, cancel_url, uid, items):
    # Set up PayPal API credentials
    client_id = "Aa-WsRJvODq4xH4iztuzJu-TXBNYB9pWNjn9Yyh1IwG10ptSweT0-gcGqDXfXdjEIk4olhHr2bVC12Se"
    secret = "EB-GVd6nrC44UVPloTpOhlhBsvAtp9fSKGzPCc42CFkzCn_7e8ud_E-wSebvxh3XusXEhtfMkCOgI4h0"
    url ="https://api-m.sandbox.paypal.com"
    # Set up API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v2/checkout/orders'

    # Request an access token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        return False,"Failed to authenticate with PayPal API",None

    access_token = token_response.json()['access_token']

    # Create payment payload
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "reference_id": uid,
            "amount": {
                  "currency_code": "EUR",
                  "value": str(amount),
                 "breakdown": {
                    "item_total": {
                        "currency_code": "EUR",
                        "value": str(amount - tax)
                    },
                     "tax_total": {
                         "currency_code": "EUR",
                         "value": str(tax)
                     },
                 },
            },
        },
    ],
        "payment_source": {
            "paypal": {
                "experience_context":
                    { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                      "payment_method_selected": "PAYPAL",
                      "brand_name": "GABRISP",
                      "locale": "en-ES",
                      "landing_page": "LOGIN",
                      "shipping_preference": "NO_SHIPPING",
                      "user_action": "PAY_NOW",
                      "return_url": "http://localhost:3000/shop/checkout/paypal/callback",
                      "cancel_url": "http://localhost:3000/shop/checkout"
                      }
            }
        }
    }


    # Create payment request
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payment_response = requests.post(payment_url, data=json.dumps(data), headers=payment_headers)
    print(payment_response.text)
    return payment_response.json()

    payment_id = payment_response.json()['id']
    approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')

    return approval_url

class PaypalView(APIView):
    def get(self, request):
        token = PaypalToken().json()
        cartID = request.GET.get('cart')
        cart_id_serializer = CartSerializer(Cart.objects.get(uid=cartID))
        cart_id = Cart.objects.get(uid=cartID)
        cart = CartItemSerializer(CartItem.objects.filter(cart_id=cart_id), many=True)
        cartItems = CartItem.objects.filter(cart_id=cart_id)
        items = [None for item in cart_id_serializer.data['products']]
        i = 0
        total = 0
        tax_total = 0
        for item in items:
            items[i] ={}

            tax = cart.data[i]['product']['price'] * 0.21
            subprice = cart.data[i]['product']['price'] - tax
            total = total + (subprice * cart.data[i]['quantity'])
            tax_total = tax_total + (tax * cart.data[i]['quantity'])

            items[i]['name'] = cart.data[i]['product']['title']
            items[i]['reference_id'] = cart.data[i]['product']['slug']
            items[i]['description'] = cart.data[i]['product']['line']
            items[i]['unit_amount'] = {}
            items[i]['unit_amount']['currency_code'] = 'EUR'
            items[i]['unit_amount']['value'] = subprice
            items[i]['tax'] = {}
            items[i]['tax']['currency_code'] = 'EUR'
            items[i]['tax']['value'] = tax
            items[i]['quantity'] = cart.data[i]['quantity']
            i = i + 1
        payment = make_paypal_payment(round(cart_id_serializer.data['total'], 2), round(cart_id_serializer.data['total'] * 0.21, 2) , "EUR", "http://hola.com", "http://hola.com", cart_id_serializer.data['uid'], items)
        return Response(data=payment)
class PaypalOrderView(APIView):
    def get(self, request):
        # Set up PayPal API credentials
        client_id = "Aa-WsRJvODq4xH4iztuzJu-TXBNYB9pWNjn9Yyh1IwG10ptSweT0-gcGqDXfXdjEIk4olhHr2bVC12Se"
        secret = "EB-GVd6nrC44UVPloTpOhlhBsvAtp9fSKGzPCc42CFkzCn_7e8ud_E-wSebvxh3XusXEhtfMkCOgI4h0"
        url = "https://api-m.sandbox.paypal.com"
        # Set up API endpoints
        base_url = url
        token_url = base_url + '/v1/oauth2/token'
        payment_url = base_url + '/v2/checkout/orders/' + request.GET.get('id')

        # Request an access token
        token_payload = {'grant_type': 'client_credentials'}
        token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

        access_token = token_response.json()['access_token']
        payment_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        data = requests.get(headers=payment_headers, url=payment_url)
        return Response(data=data.json())


class DetachPm(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            response = stripe.PaymentMethod.detach(
                request.GET.get('i')
            )
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"error":"not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
