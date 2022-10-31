from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Photo
from .serializers import PhotoSerializer
from .commands.import_photos import import_photos_from_api, import_photos_from_json


class PhotoAllView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Gets the list of all the photos.
        """
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Creates a new photo with data given in the request.
        """
        fields = ['url', 'title', 'album_id']
        data = {field_name: request.data.get(field_name) for field_name in fields}

        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetailView(APIView):
    def patch(self, request, photo_id, *args, **kwargs):
        """
        Updates the photo with the given id if exists.
        """
        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response(
                {
                    'res': 'Photo with the given id does not exist.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        fields_to_update = ['url', 'title', 'album_id']

        data = {field_name: request.data.get(field_name) for field_name in fields_to_update if
                request.data.get(field_name) is not None}

        serializer = PhotoSerializer(instance=photo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, photo_id, *args, **kwargs):
        """
        Deletes the photo with given id if exists.
        """
        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response(
                {
                    'res': 'Photo with the given id does not exist.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        photo.delete()
        return Response(
            {
                'res': 'Photo successfully deleted.'
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def import_data_from_api(request):
    import_photos_from_api()


@api_view(['POST'])
def import_data_from_json(request):
    import_photos_from_json()
