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
from common.pagination import CustomPageNumberPagination
from django.db.models import Q

# Create your views here
class ContactApi(APIView):
    serializer_class=ContactSerializers
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            ALLOWED_PARAMS = {"is_active", "is_read", "is_important", "created_at", "search", "page", "page_size"}
            unexpected = set(request.query_params.keys()) - ALLOWED_PARAMS
            if unexpected:
                return Response(
                    {"detail": f"Unexpected query parameter(s): {', '.join(unexpected)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                contacts = ContactModel.objects.all().order_by("-id")

                # Sorting by created_at
                try:
                    created_at = request.query_params.get("created_at", None)
                    if created_at:
                        if created_at == "latest":
                            contacts = contacts.order_by("-created_at")
                        elif created_at == "oldest":
                            contacts = contacts.order_by("created_at")
                        else:
                            contacts = contacts.order_by("-id")
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Filter by is_active
                try:
                    is_active = request.query_params.get("is_active", None)
                    if is_active is not None:
                        if is_active.lower() == 'true':
                            contacts = contacts.filter(is_active=True)
                        elif is_active.lower() == 'false':
                            contacts = contacts.filter(is_active=False)
                        else:
                            return Response({'detail': 'Invalid value for is_active. Must be "true" or "false".'},
                                            status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Filter by is_read
                try:
                    is_read = request.query_params.get("is_read", None)
                    if is_read is not None:
                        if is_read.lower() == 'true':
                            contacts = contacts.filter(is_read=True)
                        elif is_read.lower() == 'false':
                            contacts = contacts.filter(is_read=False)
                        else:
                            return Response({'detail': 'Invalid value for is_read. Must be "true" or "false".'},
                                            status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Filter by is_important
                try:
                    is_important = request.query_params.get("is_important", None)
                    if is_important is not None:
                        if is_important.lower() == 'true':
                            contacts = contacts.filter(is_important=True)
                        elif is_important.lower() == 'false':
                            contacts = contacts.filter(is_important=False)
                        else:
                            return Response({'detail': 'Invalid value for is_important. Must be "true" or "false".'},
                                            status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Search by name or email
                try:
                    search = request.query_params.get("search", None)
                    if search:
                        contacts = contacts.filter(Q(name__icontains=search) | Q(email__icontains=search))
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Pagination
                paginator = CustomPageNumberPagination()
                paginated_queryset = paginator.paginate_queryset(contacts, request)
                serializer = ContactSerializers(paginated_queryset, many=True, context={"request": request})
                return paginator.get_paginated_response(serializer.data)

            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                contact = ContactModel.objects.get(id=pk)
                serializer = ContactSerializers(contact, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ContactModel.DoesNotExist:
                return Response({'detail': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        
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
        
      
    
    