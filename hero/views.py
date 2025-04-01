
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from hero.models import Hero
from common.models import ImageContent,Image
from .serializer import HeroSerializers,ImageContentSerializer


class HeroApi(APIView):
    def get(self,request,pk=None):
        if pk is None:
            heroes=Hero.objects.all()
            if not heroes:
                return Response({'message':"Hero not found"},status=status.HTTP_404_NOT_FOUND)
            hero_data=[]
            for hero in heroes:
                hero_serializer = HeroSerializers(hero, context={'request': request})
                
                # Fetch images for the hero
                images = ImageContent.objects.filter(content_type=ContentType.objects.get_for_model(Hero), object_id=hero.id)
                image_serializer = ImageContentSerializer(images, many=True, context={'request': request})

                hero_data.append({
                    "hero": hero_serializer.data,
                    "images": image_serializer.data
                })

            return Response(hero_data, status=status.HTTP_200_OK)

        else:
            try:
                # Fetch a specific Hero by ID
                hero = Hero.objects.get(pk=pk)
                hero_serializer = HeroSerializers(hero, context={'request': request})

                # Fetch images for the specific hero
                images = ImageContent.objects.filter(content_type=ContentType.objects.get_for_model(Hero), object_id=hero.id)
                image_serializer = ImageContentSerializer(images, many=True, context={'request': request})

                return Response({
                    "hero": hero_serializer.data,
                    "images": image_serializer.data
                }, status=status.HTTP_200_OK)

            except Hero.DoesNotExist:
                return Response({'message': "Hero not found"}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request):
        # Initialize the serializer with incoming data
        hero_serializer = HeroSerializers(data=request.data, context={'request': request})

        if hero_serializer.is_valid():
            # The hero creation and image attachment is handled by the serializer
            hero = hero_serializer.save()

            return Response({
                'message': "Hero created successfully with images."
            }, status=status.HTTP_201_CREATED)
        
        return Response(hero_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

