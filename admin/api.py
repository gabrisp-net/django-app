from rest_framework.views import APIView as Base
from rest_framework.response import Response
from rest_framework import status

class APIView(Base):
    def get(self):
        return Response(status=status.HTTP_200_OK, data={"auth": "http://127.0.0.1:8000/api/auth/","products": "http://127.0.0.1:8000/api/products/","cart": "http://127.0.0.1:8000/api/cart/",})