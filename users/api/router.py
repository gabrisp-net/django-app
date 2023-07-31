from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.status import HTTP_200_OK
from users.api.views import UserBillingView, UserUpdateView, UserPasswordUpdate
from . import views

class LoginView(TokenObtainPairView):
    pass
decorated_login_view = swagger_auto_schema(method="POST",operation_description="Login User", operation_id="accountLogin")(LoginView.as_view())

urlpatterns = [
    path('account/login/', decorated_login_view, name="token_obtain_pair_view"),
    path('account/addresses/', UserBillingView.as_view()),
    path('account/', UserUpdateView.as_view()),
    path('account/password/', UserPasswordUpdate.as_view()),
    path('e/', views.signupView),
    path('account/activate/<uidb64>/<token>/',views.ActivateUser.as_view())
]