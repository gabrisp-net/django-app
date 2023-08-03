from email.message import EmailMessage

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.utils import  timezone
from django.utils.encoding import force_str
from drf_yasg.utils import swagger_auto_schema
from nanoid import generate
from rest_framework.viewsets import ViewSet
from rest_framework.views import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from users.api.serializer import UserSerializer, UserRegisterSerializer, UserBillingSerializer
from rest_framework.views import APIView
from users.models import UserBilling
from .tokens import account_activation_token
from django.template.loader import get_template
from django.template.loader import render_to_string
import os
import stripe
#EMAIL
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


#CONFIRM EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.api.tokens import account_activation_token
from users.models import User

from orders.api.serializers import OrderSerializer
from orders.models import Order

stripe.api_key = os.getenv('SK')

class UserSubscriberView(APIView):
    def post(self, request):
        password = generate("0123456789abcefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ!?¿*$%&/()=", 10)
        serializer = UserRegisterSerializer(data={'first_name': request.data['first_name'],'last_name' :request.data['last_name'],"email":request.data['email'],"password": password})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            subject = f'Hello {user.first_name} please confirm your account'
            message = ''
            email_from = f'Gabrisp <{settings.EMAIL_HOST_USER}>'
            recipient_list = [serializer.data['email'], ]
            html_content = render_to_string('emails/confirmEmailSubscription.html', {
                'name': serializer.data['first_name'] + " " + serializer.data['last_name'],
                "password": password,
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),

            })  # render with dynamic value
            send_mail(subject, message, email_from, recipient_list, html_message=html_content)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserViewSet(ViewSet):
    @swagger_auto_schema(operation_description="Returns the logged in user, if present", operation_id="accountData" , operation_security="JWT")
    def list(self, request):
            if request.user.is_authenticated:
                serializer = UserSerializer(request.user)
                request.user.last_login = timezone.now()
                request.user.save()
                return Response(status=HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=HTTP_401_UNAUTHORIZED, data={"error":{"code": 401, "message":"User not found."}})
   # @swagger_auto_schema(operation_description="Register User", operation_id="accountCreate")



class UserUpdateView(APIView):
    def get(self, request):
            if request.user.is_authenticated:
                serializer = UserSerializer(request.user)
                request.user.last_login = timezone.now()
                request.user.save()
                return Response(status=HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=HTTP_401_UNAUTHORIZED, data={"error":{"code": 401, "message":"User not found."}})
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            print(User.objects.get(email=serializer.data['email']).pk)
            print(serializer.data)
            current_site = get_current_site(request)
            subject = f'Hello {user.first_name} please confirm your account'
            message = ''
            email_from = f'Gabrisp <{settings.EMAIL_HOST_USER}>'
            recipient_list = [serializer.data['email'], ]
            html_content = render_to_string('emails/confirmEmail.html', {
                'name': serializer.data['first_name'] +" " +  serializer.data['last_name'],
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),

            })  # render with dynamic value
            send_mail(subject, message, email_from, recipient_list, html_message=html_content)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if request.user.is_authenticated:
            request.user.last_name = request.data['last_name']
            request.user.first_name = request.data['first_name']
            request.user.email = request.data['email']
            request.user.save()
            serializer = UserSerializer(request.user)
            #request.user.last_login = timezone.now()
            return Response(status=HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data={"error": {"code": 401, "message": "User not found."}})

class UserBillingView(APIView):
     def get(self, request):
          if request.user.is_authenticated:
                info = UserBilling.objects.filter(user_id=request.user)
                print(request.user)
                serializer = UserBillingSerializer(info, many=True)
                return Response(status=HTTP_200_OK,data=serializer.data)
          else:
                return Response(status=HTTP_401_UNAUTHORIZED, data={"detail": "Not authenticated"})
     def post(self, request):
        if request.user.is_authenticated:
            print(request.data)
            address = UserBilling.objects.create(
                user_id = request.user,
                name=request.data['name'],
                street=request.data['street'],
                country=request.data['country'],
                state=request.data['state'],
                city=request.data['city'],
                postalCode=request.data['postalCode']
            )
            return Response(status=HTTP_200_OK, data="ok")
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data={"detail": "Not authenticated"})
     def put(self, request):
        if request.user.is_authenticated:
            address = UserBilling.objects.filter(user_id=request.user, id=request.data['id'])
            if len(address) > 0:
                address[0].name = request.data['name']
                address[0].street = request.data['street']
                address[0].country = request.data['country']
                address[0].state = request.data['state']
                address[0].city = request.data['city']
                address[0].postalCode = request.data['postalCode']
                address[0].save()
                return Response(status=HTTP_200_OK, data="ok")
            else:
                return Response(status=HTTP_401_UNAUTHORIZED, data={"detail": "Address not finded."})
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data={"detail": "Not authenticated"})




class UserPasswordUpdate(APIView):
    def post(self, request):
        print("request.POST")
        if request.user.is_authenticated:
            user = request.user
            if (user.check_password(request.data['oldPassword'])):
                if request.data['password'] == request.data['repeatPassword']:
                    user.set_password(request.data['password'])
                    user.save()
                    serializer = UserSerializer(user)
                    return Response(status=HTTP_200_OK, data=serializer.data)
                else:
                    return Response(status=HTTP_200_OK, data={"error": "New Passwords dont Match"})
            else:
                return Response(status=HTTP_401_UNAUTHORIZED, data={"error": "Old Password Invalid"})
        else:
            return Response(status=HTTP_401_UNAUTHORIZED, data={"error": "Not authenticated"})



def signupView(request):
        subscription = stripe.Subscription.retrieve(id="sub_1NZg4RIR4r0iQIWOsAbi6Hfq")
        payment = stripe.PaymentMethod.retrieve(id=subscription['default_payment_method'])
        p = {}
        p['id'] = payment.id
        p['brand'] = payment.card.brand
        p['last4'] = payment.card.last4
        p['exp'] = {}
        p['exp']['month'] = payment.card.exp_month
        p['exp']['year'] = payment.card.exp_year
        p['icon'] = 'https://gabrisp-development.s3.amazonaws.com/icons/icon-payment-' + p['brand'] + '.svg'
        print(p)
        return render(request, 'emails/subscriptionConfirmation.html', {"subscription": subscription,
                                                                        "payment_method": p,
                                                                 "user":{
                                                                     "email": "gabrielsanpal@gmail.com",
                                                                     "first_name": "Gabriel",
                                                                     "last_name": "Sanchez"
                                                                 }})


class ActivateUser(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and account_activation_token.check_token(user, token):
            if user.is_active == False:
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response(status=HTTP_200_OK, data={'status': 'succeed',
                                                      'refresh': str(refresh),
                                                      'access': str(refresh.access_token)
                                                      })
            else:
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response(status=HTTP_200_OK, data={'status': 'already_confirmed',
                                                          })
                                                                       # subject = f'Welcome {user.first_name}!'
                                                                        #email_from = f'Gabrisp <{settings.EMAIL_HOST_USER}>'
                                                                       # recipient_list = [user.email, ]
                                                                       ### html_content = render_to_string('emails/signup.html', {
                                                                      ##      'name': user.first_name + " " +  user.last_name,
                                                                        #})
                                                                        #send_mail(subject, "", email_from, recipient_list, html_message=html_content)
        return Response(status=HTTP_401_UNAUTHORIZED, data={"status": "failed"})