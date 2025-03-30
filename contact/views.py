from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from contact.models import ContactModel
from contact.serializers import ContactSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



# Create your views here
class ContactApi(APIView):
    serializer_class=ContactSerializers
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]

    def get (self,request,pk=None):
        if pk is None:
            try:
                contacts=ContactModel.objects.all()
                if not contacts:
                    return Response({'detail':'No contacts Found'},status=status.HTTP_404_NOT_FOUND)
                serializer=ContactSerializers(contacts,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                contact=ContactModel.objects.get(id=pk)
                serializer=ContactSerializers(contact)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

        
    def post(self,request):
        try:
            serializer=ContactSerializers(data=request.data)
            if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data,status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  
                    return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request,pk):
        try:
          contact = ContactModel.objects.get(id=pk)
        except ContactModel.DoesNotExist:
           
            return Response({'message': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ContactSerializers(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Use 200 OK for updates
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        try:
            contact=ContactModel.objects.get(id=pk)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        serializers=ContactSerializers(contact,data=request.data,partial=True)
        if serializers.is_valid(): 
             serializers.save()   
             return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            contact = ContactModel.objects.get(id=pk)
            contact.delete()
            return Response({'message': 'Contact deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ContactModel.DoesNotExist:
            return Response({'message': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
      
    
    