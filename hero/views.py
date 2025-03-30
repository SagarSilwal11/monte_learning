# from django.shortcuts import render,redirect,get_object_or_404
# from django.http import HttpResponse
# from .forms import HeroForm
# from .serializer import HeroSerializers
# from .models import Hero
# from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
# class HeroApi(ModelViewSet):

#     queryset=Hero.objects.all()
#     serializer_class=HeroSerializers
#     renderer_classes=[JSONRenderer,BrowsableAPIRenderer]
   

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hero.models import Hero
from hero.serializer import HeroSerializers

class HeroApi(APIView):
    serializer_class = HeroSerializers

    def get(self, request, pk=None):
        if pk is None:
            try:
                heroes = Hero.objects.all()
                if not heroes:
                    return Response({'detail': 'No heroes found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = HeroSerializers(heroes, many=True,context={"request":request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                hero = Hero.objects.get(id=pk)
                serializer = HeroSerializers(hero,context={"request":request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Hero.DoesNotExist:
                return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = HeroSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            hero = Hero.objects.get(id=pk)
        except Hero.DoesNotExist:
            return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HeroSerializers(hero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            hero = Hero.objects.get(id=pk)
        except Hero.DoesNotExist:
            return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HeroSerializers(hero, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            hero = Hero.objects.get(id=pk)
            hero.delete()
            return Response({'detail': 'Hero deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Hero.DoesNotExist:
            return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
