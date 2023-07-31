from rest_framework import status
from rest_framework.views import APIView
from products.models import ProductImage, ProductDowload, Product
from wsgiref.util import FileWrapper
import stripe
import os
from rest_framework.response import Response
from django.http import FileResponse,HttpResponse
from rest_framework import  status

class DownloadView(APIView):
    def get(self, request, download):
        downloads = ProductDowload.objects.filter(uid=download)
        if len(downloads) > 0 :
            download = downloads[0]
            fn = download.product_id.file.name.split(".")
            # get an open file handle (I'm just using a file attached to the model for this example):
            if download.left > 0:
                file_handle = download.product_id.file.open()
                # send file
                response = FileResponse(file_handle, content_type='whatever')
                response['Content-Length'] = download.product_id.file.size
                response['Content-Disposition'] = 'attachment; filename="' + "download-" + download.uid + "0" + str(download.left) + "-" + download.product_id.slug  + "."+ fn[1] + '"'
                download.left = download.left - 1
                download.save()
                return response
            elif download.left == -3:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "no intents left, query not found"})
            else :
                download.left = download.left - 1
                download.save()
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "no intents left"})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "no intents left, query not found"})
