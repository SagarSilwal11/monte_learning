from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# importing the models

from hero.models import Hero
from facilities.models import Facilities
from activities.models import ActivitiesModel
from contact.models import ContactModel

# importing the serializers
from hero.serializer import HeroSerializers
from facilities.serializers import FacilitySerializer
from activities.serializers import ActivitiesModelSerializers
from contact.serializers import ContactSerializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# For the Permission and Group
from rest_framework import serializers
from rest_framework.views import APIView
from common.serializers import AssignGroupSerializer,AssignPermissionSerializer
from rest_framework import status

# for the custom JWTTOken logic
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,) 

class CommonApi(APIView):
    serializer_class=HeroSerializers
    authentication_classes=[]
    permission_classes=[AllowAny]

    def get(self,request):
        heros=Hero.objects.all()
        facilities=Facilities.objects.all()
        activities=ActivitiesModel.objects.all()
        contact=ContactModel.objects.all()

        hero_data=HeroSerializers(heros,many=True,context={'request':request}).data
        facilities_data=FacilitySerializer(facilities,many=True,context={'request':request}).data
        activities_data=ActivitiesModelSerializers(activities,many=True,context={'request':request}).data
        contact_data=ContactSerializers(contact,many=True,context={'request':request}).data
    
        combined_data={
        'heros':hero_data,
        'facilities':facilities_data,
        'activities':activities_data,
        'contact':contact_data
        }
    
        return Response(combined_data,status=status.HTTP_200_OK)
    
    



class AssignPermissionApi(viewsets.ViewSet):
    def create(self,request):
        serializers=AssignPermissionSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'permission assigned sucessfully'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class AssignGroupApi(viewsets.ViewSet):

    def create(self,request):
        serializers=AssignGroupSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message":'Group Assign sucessfully'},xstatus=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



