#from .settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from .router import router
from cart.api.models import CartAddItemAPIView, CartRemoveItemAPIView, CartIsIn, DeleteCart
from orders.stripe.views import PaymentIntentView, CardViews, CustomerView, PaymentMethodView, PaypalView, PaypalOrderView, DetachPm
from orders.downloads.views import DownloadView
from orders.api.views import OrderView, getOrderView, getOrders
from users.api.views import UserSubscriberView
from members.api.views import ItemsMemberships, MembershipsView, ProductMembersView, ItemMembersView, VideoMembersView, MembershipView, MembershipIntent, SubscriptionView, CancelSubscriptionView, StopCancelSubscriptionView, AsapCancelSubscriptionView, MethodUpdateView, AttachMethod, OtherMemberships, ProductsMemberships, VideosMemberships

schema_view = get_schema_view(
    openapi.Info(
        title="Documentation",
        default_version='v1',
    ),
   public=True,
)
admin.site.site_header = 'Gabrisp Admin'
admin.site.site_title = 'Gabrisp'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),
    #path('docs/tester/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/', include(router.urls)),
    path('api/', include('users.api.router')),
    path('api/cart/<str:cart>/add/<str:product>/', CartAddItemAPIView.as_view()),
    path('api/cart/<str:cart>/remove/<str:product>/', CartRemoveItemAPIView.as_view()),
    path('api/cart/<str:cart>/delete/', DeleteCart.as_view()),
    path('api/cart/<str:cart>/<str:product>/', CartIsIn.as_view()),
    path('api/stripe/intent/create/', PaymentIntentView.as_view()),
    path('api/stripe/customer/cards/', CardViews.as_view()),
    path('api/download/<str:download>/', DownloadView.as_view()),
    path('api/orders/<str:id>/', getOrderView.as_view()),
    path('api/account/orders/', getOrders.as_view()),
    path('api/orders/', OrderView.as_view()),
    path('api/stripe/customer/', CustomerView.as_view()),
    path('api/stripe/method/<str:id>', PaymentMethodView.as_view()),
    path('api/paypal/', PaypalView.as_view()),
    path('api/paypal/order/', PaypalOrderView.as_view()),
    path('api/stripe/customer/method/detach/', DetachPm.as_view()),
    path('api/stripe/customer/method/attach/<str:id>/', AttachMethod.as_view()),
    path('api/members/content/',ItemsMemberships.as_view()),
    path('api/members/data/',MembershipsView.as_view()),
    path('api/members/data/<int:id>/',MembershipView.as_view()),
    path('api/members/products/<str:slug>/', ProductMembersView.as_view()),
    path('api/members/products/', ProductsMemberships.as_view()),
    path('api/members/other/', OtherMemberships.as_view()),
    path('api/members/videos/', VideosMemberships.as_view()),
    path('api/members/other/<str:slug>/', ItemMembersView.as_view()),
    path('api/members/video/<str:slug>/', VideoMembersView.as_view()),
    path('api/members/subscription/', SubscriptionView.as_view()),
    path('api/members/intent/<str:id>/', MembershipIntent.as_view()),
    path('api/members/subscription/cancel/<str:id>/', CancelSubscriptionView.as_view()),
    path('api/members/subscription/cancel/stop/<str:id>/', StopCancelSubscriptionView.as_view()),
    path('api/members/subscription/cancel/asap/<str:id>/', AsapCancelSubscriptionView.as_view()),
    path('api/members/subscription/method/update/<str:id>/<str:pm>/', MethodUpdateView.as_view()),
    path('api/account/subscribe/', UserSubscriberView.as_view())
] #+ static(MEDIA_URL, document_root=MEDIA_ROOT) CancelSubscriptionView StopCancelSubscriptionView



#handler404 = 'products.views.handler404'
