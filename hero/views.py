
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from hero.models import Hero
# from hero.serializer import HeroSerializers

# class HeroApi(APIView):
#     serializer_class = HeroSerializers

#     def get(self, request, pk=None):
#         if pk is None:
#             try:
#                 heroes = Hero.objects.all()
#                 if not heroes:
#                     return Response({'detail': 'No heroes found'}, status=status.HTTP_404_NOT_FOUND)
#                 serializer = HeroSerializers(heroes, many=True,context={"request":request})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             try:
#                 hero = Hero.objects.get(id=pk)
#                 serializer = HeroSerializers(hero,context={"request":request})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Hero.DoesNotExist:
#                 return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):
#         try:
#             serializer = HeroSerializers(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             hero = Hero.objects.get(id=pk)
#         except Hero.DoesNotExist:
#             return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = HeroSerializers(hero, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         try:
#             hero = Hero.objects.get(id=pk)
#         except Hero.DoesNotExist:
#             return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = HeroSerializers(hero, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             hero = Hero.objects.get(id=pk)
#             hero.delete()
#             return Response({'detail': 'Hero deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except Hero.DoesNotExist:
#             return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from hero.models import Hero
from common.models import ImageContent
from .serializer import HeroSerializers,ImageContentSerializer


class HeroApi(APIView):
    def get(self,request,pk=None):
        if pk is None:
            heroes=Hero.objects.all()
            if not heroes:
                return Response({'message':"Hero not found"},status=status.HTTP_404_NOT_FOUND)
            serializer=HeroSerializers(many=True,context={'request':request})
            hero_data=[]
            for hero in heroes:
                hero_serializer=HeroSerializers(hero,context={'request':request})

                images=ImageContent.objects.filter(content_type=ContentType.objects.get_for_model(Hero),object_id=hero.id)
                image_serializer=ImageContentSerializer(images,many=True)
                hero_data.append({
                    "hero":hero_serializer.data,
                    "images":image_serializer.data
                })
            return Response(hero_data,status=status.HTTP_200_OK)
        else:
            # Handle fetching a specific hero
            try:
                hero = Hero.objects.get(pk=pk)
                hero_serializer = HeroSerializers(hero, context={'request': request})
                
                images = ImageContent.objects.filter(content_type=ContentType.objects.get_for_model(Hero), object_id=hero.id)
                image_serializer = ImageContentSerializer(images, many=True, context={'request': request})
                
                return Response({
                    "hero": hero_serializer.data,
                    "images": image_serializer.data
                }, status=status.HTTP_200_OK)
            
            except Hero.DoesNotExist:
                return Response({'message': "Hero not found"}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self,request):
        hero_serializer=HeroSerializers(data=request.data)
        if hero_serializer.is_valid():
            hero=hero_serializer.save()
            image_data=request.FILES.get('url')
            if image_data:
                ImageContent.objects.create(content_type=ContentType.objects.get_for_model(Hero),object_id=hero.id,url=image_data)
            else:
                return Response({'message':'please provide the images'},status=status.HTTP_400_BAD_REQUEST)
            return Response({
            'message':"hero created "
            },status=status.HTTP_201_CREATED)
        
        return Response(hero_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    

