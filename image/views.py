from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
import json
import requests
import hashlib
import imagehash
from PIL import Image as PILImage, UnidentifiedImageError
from io import BytesIO

class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all().order_by('-created_at')
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        link = request.data.get("link")

        if not link:
            return Response({"error":"The image URL is missing"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(link)


        try:
            image_binary = BytesIO(response.content)
            image = PILImage.open(image_binary)
            
            md5_hash = hashlib.md5(response.content).hexdigest()
            p_hash = str(imagehash.phash(image))
            

            entry = Image.objects.create(p_hash=p_hash, md5_hash=md5_hash, link=link)

            return Response({"md5_hash":md5_hash, "p_hash":p_hash, "unique_id":entry.id}, status=status.HTTP_201_CREATED)
        except UnidentifiedImageError as e:
            return Response({"error": f"UnidentifiedImageError error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        unique_id = kwargs.get('pk')
        link = request.data.get("link")

        if not (link and unique_id):
            return Response({"error":"The image URL is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Image.objects.filter(id=unique_id).exists():
            return Response({"error":"The desired entry does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

        response = requests.get(link)
 

        try:
            image_binary = BytesIO(response.content)
            image = PILImage.open(image_binary)
            
            md5_hash = hashlib.md5(response.content).hexdigest()
            p_hash = str(imagehash.phash(image))
            

            serializer = self.get_serializer(instance, data={'link': link, 'md5_hash': md5_hash, 'p_hash': p_hash}, partial=True)
            if serializer.is_valid():
                updated_instance = serializer.save()

            return Response({"md5_hash":md5_hash, "p_hash":p_hash, "unique_id":updated_instance.id}, status=status.HTTP_200_OK)
        except AssertionError as e:
            return Response({"error": f"Assertion error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except UnidentifiedImageError as e:
            return Response({"error": f"UnidentifiedImageError error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        unique_id = kwargs.get('pk')

        if not Image.objects.filter(id=unique_id).exists():
            return Response({"error":"The desired entry does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        instance = Image.objects.get(id=unique_id)
        instance.delete()

        return Response({"message":"The entry has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)