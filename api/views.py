from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Photo
from .serializers import PhotoSerializer


class RESTAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Get the list of all the photos
        """
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new photo with data given in the request
        """
        data = {
            'url': request.data.get('url'),
            'title': request.data.get('title'),
            'album_id': request.data.get('album_id')
        }

        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
