from rest_framework.routers import DefaultRouter
from products.api.models import ProductAPIView, TagAPIView
from cart.api.models import CartAPIView
from users.api.views import UserViewSet
router = DefaultRouter()


router.register(prefix="products/tags", basename="products/tags", viewset=TagAPIView)
router.register(prefix="products", basename="products", viewset=ProductAPIView)
router.register(prefix="cart", basename="cart", viewset=CartAPIView)
#router.register(prefix="account", basename="account", viewset=UserViewSet)

