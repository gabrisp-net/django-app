import stripe
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from members.api.serializers import Locked_ItemMembers, Locked_ProductMembers, Locked_VideoMembers
from members.models import ProductMembership, ItemMembership, VideoMembership, Membership
from django.http import JsonResponse
from members.api.serializers import Unlocked_VideoMembers, Unlocked_ItemMembers, Unlocked_ProductMembers, OneMembershipSerializer

from products.models import Product

class AttachMethod(APIView):
    def post(self, request, id):
        data = stripe.PaymentMethod.attach(
            id,
            customer=request.user.stripe,
        )
        return Response(status=status.HTTP_200_OK, data=data)

class MethodUpdateView(APIView):
    def post(self, request, id, pm):
        subscription = stripe.Subscription.retrieve(id, expand=['latest_invoice.payment_intent'],)
        response = stripe.Subscription.modify(
        id,
        default_payment_method=pm,
        payment_behavior='error_if_incomplete'
        )
        print(subscription)
        if subscription['latest_invoice']['amount_due'] != subscription['latest_invoice']['amount_paid']:
           stripe.Invoice.pay(subscription['latest_invoice'])
        return Response(status=status.HTTP_200_OK, data=response)

class AsapCancelSubscriptionView(APIView):
    def post(self, request, id):
        response = stripe.Subscription.delete(
        id,
        )
        return Response(status=status.HTTP_200_OK, data=response)

class CancelSubscriptionView(APIView):
    def post(self, request, id):
        response = stripe.Subscription.modify(
        id,
        cancel_at_period_end=True,
        )
        return Response(status=status.HTTP_200_OK, data=response)

class StopCancelSubscriptionView(APIView):
    def post(self, request, id):
        response = stripe.Subscription.modify(
        id,
        cancel_at_period_end=False,
        )
        return Response(status=status.HTTP_200_OK, data=response)

class SubscriptionView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            subscriptions = stripe.Subscription.list(customer=request.user.stripe, expand=['data.latest_invoice'])
            if not subscriptions.data:
                request.user.subscription = False
                request.user.save()
                return Response(status=status.HTTP_200_OK, data={"detail": "none"})
            elif subscriptions.data[0].status == "active":
                print("active")
                request.user.subscription = True
                infomem = OneMembershipSerializer(Membership.objects.get(id_stripe=subscriptions.data[0].plan.id))
                request.user.save()
            else:
                request.user.subscription = False
                infomem = OneMembershipSerializer(Membership.objects.get(id_stripe=subscriptions.data[0].plan.id))
                request.user.save()
            return Response(status=status.HTTP_200_OK, data={**subscriptions.data[0],"mine": infomem.data})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "not authenticated"})


class MembershipIntent(APIView):
    def get(self, request, id):
        if request.user.is_authenticated and request.GET.get('save_card'):
            member = Membership.objects.get(id=id)
            subscriptions = stripe.Subscription.list(customer=request.user.stripe)
            for s in subscriptions:
                stripe.Subscription.delete(s['id'])
            subscription = stripe.Subscription.create(
                customer=request.user.stripe,
                items=[{
                    'price': member.id_stripe,
                }],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
            )
            return Response(status=status.HTTP_200_OK, data=subscription)
        elif request.user.is_authenticated and request.GET.get('pi'):
            member = Membership.objects.get(id=id)
            subscriptions = stripe.Subscription.list(customer=request.user.stripe)
            for s in subscriptions:
                stripe.Subscription.delete(s['id'])
            subscription = stripe.Subscription.create(
                customer=request.user.stripe,
                items=[{
                    'price': member.id_stripe,
                }],
                default_payment_method=request.GET.get('pi'),
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
            )
            return Response(status=status.HTTP_200_OK, data=subscription)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "not authenticated"})


class MembershipView(APIView):
    def get(self, request, id):
        data = OneMembershipSerializer(Membership.objects.get(id=id))
        return Response(status=status.HTTP_200_OK, data=data.data)


class MembershipsView(APIView):
    def get(self, request):
        data = OneMembershipSerializer(Membership.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class ItemsMemberships(APIView):
    def get(self, request):
        if request.user.is_authenticated and (request.user.subscription is True):
            products = Unlocked_ProductMembers(ProductMembership.objects.all(),many=True)
            items = Unlocked_ItemMembers(ItemMembership.objects.all(),many=True)
            videos = Unlocked_VideoMembers(VideoMembership.objects.all(),many=True)
            public = [*products.data, *items.data, *videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public})
        elif request.user.is_authenticated:
            products = Unlocked_ProductMembers(ProductMembership.objects.filter(visibility=0), many=True)
            items = Unlocked_ItemMembers(ItemMembership.objects.filter(visibility=0), many=True)
            videos = Unlocked_VideoMembers(VideoMembership.objects.filter(visibility=0), many=True)
            public = [*products.data, *items.data, *videos.data]
            private_products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=1), many=True)
            private_items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=1), many=True)
            private_videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=1), many=True)
            private = [*private_products.data, *private_items.data, *private_videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public, 'private': private})
        else:
            products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=0), many=True)
            items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=0), many=True)
            videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=0), many=True)
            public = [*products.data, *items.data, *videos.data]
            private_products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=1), many=True)
            private_items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=1), many=True)
            private_videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=1), many=True)
            private = [*private_products.data, *private_items.data, *private_videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public,'private': private})

class OtherMemberships(APIView):
    def get(self, request):
        if request.user.is_authenticated and (request.user.subscription is True):
            items = Unlocked_ItemMembers(ItemMembership.objects.all(),many=True)
            public = [*items.data]
            return Response(status=status.HTTP_200_OK, data={'public': public})
        elif request.user.is_authenticated:
            items = Unlocked_ItemMembers(ItemMembership.objects.filter(visibility=0), many=True)
            public = [*items.data]
            private_items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=1), many=True)
            private = [ *private_items.data]
            return Response(status=status.HTTP_200_OK, data={'public': public, 'private': private})
        else:
            items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=0), many=True)
            public = [*items.data]
            private_items = Locked_ItemMembers(ItemMembership.objects.filter(visibility=1), many=True)
            private = [*private_items.data]
            return Response(status=status.HTTP_200_OK, data={'public': public,'private': private})


class ProductsMemberships(APIView):
    def get(self, request):
        if request.user.is_authenticated and (request.user.subscription is True):
            products = Unlocked_ProductMembers(ProductMembership.objects.all(),many=True)
            public = [*products.data]
            return Response(status=status.HTTP_200_OK, data={'public': public})
        elif request.user.is_authenticated:
            products = Unlocked_ProductMembers(ProductMembership.objects.filter(visibility=0), many=True)
            public = [*products.data]
            private_products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=1), many=True)
            private = [*private_products.data]
            return Response(status=status.HTTP_200_OK, data={'public': public, 'private': private})
        else:
            products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=0), many=True)
            public = [*products.data]
            private_products = Locked_ProductMembers(ProductMembership.objects.filter(visibility=1), many=True)
            private = [*private_products.data]
            return Response(status=status.HTTP_200_OK, data={'public': public,'private': private})

class VideosMemberships(APIView):
    def get(self, request):
        if request.user.is_authenticated and (request.user.subscription is True):
            videos = Unlocked_VideoMembers(VideoMembership.objects.all(),many=True)
            public = [*videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public})
        elif request.user.is_authenticated:
            videos = Unlocked_VideoMembers(VideoMembership.objects.filter(visibility=0), many=True)
            public = [*videos.data]
            private_videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=1), many=True)
            private = [*private_videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public, 'private': private})
        else:
            videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=0), many=True)
            public = [*videos.data]
            private_videos = Locked_VideoMembers(VideoMembership.objects.filter(visibility=1), many=True)
            private = [*private_videos.data]
            return Response(status=status.HTTP_200_OK, data={'public': public,'private': private})

class ProductMembersView(APIView):
    def get(self, request, slug):
        response = {}
        if request.user.is_authenticated and (request.user.subscription is True):
            response['locked'] = False
            product = Unlocked_ProductMembers(ProductMembership.objects.get(product_id__slug=slug))
        elif request.user.is_authenticated:
            response['locked'] = False
            product = Unlocked_ProductMembers(ProductMembership.objects.get(product_id__slug=slug))
        else:
            response['locked'] = True
            product = Locked_ProductMembers(ProductMembership.objects.get(product_id__slug=slug))
        response = {**response, **product.data}
        return Response(status=status.HTTP_200_OK, data=response)


class ItemMembersView(APIView):
    def get(self, request, slug):
        response = {}
        it = ItemMembership.objects.get(slug=slug)
        if request.user.is_authenticated and (request.user.subscription is True):
            response['locked'] = False
            product = Unlocked_ItemMembers(ItemMembership.objects.get(slug=slug))
        elif request.user.is_authenticated and (request.user.subscription is False) and it.visibility is 0 :
            response['locked'] = False
            product = Unlocked_ItemMembers(ItemMembership.objects.get(slug=slug))
        elif request.user.is_authenticated and (request.user.subscription is False) and it.visibility is 1 :
            response['locked'] = True
            product = Locked_ItemMembers(ItemMembership.objects.get(slug=slug))
        else:
            response['locked'] = True
            product = Locked_ItemMembers(ItemMembership.objects.get(slug=slug))
        response = {**response, **product.data}
        return Response(status=status.HTTP_200_OK, data=response)


class VideoMembersView(APIView):
    def get(self, request, slug):
        response = {}
        it = VideoMembership.objects.get(slug=slug)
        if request.user.is_authenticated and (request.user.subscription is True):
            response['locked'] = False
            product = Unlocked_VideoMembers(VideoMembership.objects.get(slug=slug))
        elif request.user.is_authenticated and (request.user.subscription is False) and it.visibility is 0:
            response['locked'] = False
            product = Unlocked_VideoMembers(VideoMembership.objects.get(slug=slug))
        elif request.user.is_authenticated and (request.user.subscription is False) and it.visibility is 1:
            response['locked'] = True
            product = Locked_VideoMembers(VideoMembership.objects.get(slug=slug))
        else:
            response['locked'] = True
            product = Locked_VideoMembers(VideoMembership.objects.get(slug=slug))
        response = {**response, **product.data}
        return Response(status=status.HTTP_200_OK, data=response)