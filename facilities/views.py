from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facilities.models import Facilities
from facilities.serializers import FacilitySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class FacilityApi(APIView):
    serializer_class = FacilitySerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                facilities = Facilities.objects.all()
                if not facilities:
                    return Response({'detail': 'No facilities found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = FacilitySerializer(facilities, many=True,context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                facility = Facilities.objects.get(id=pk)
                serializer = FacilitySerializer(facility,context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Facilities.DoesNotExist:
                return Response({'detail': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = FacilitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            facility = Facilities.objects.get(id=pk)
        except Facilities.DoesNotExist:
            return Response({'detail': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FacilitySerializer(facility, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            facility = Facilities.objects.get(id=pk)
        except Facilities.DoesNotExist:
            return Response({'detail': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FacilitySerializer(facility, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            facility = Facilities.objects.get(id=pk)
            facility.delete()
            return Response({'detail': 'Facility deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Facilities.DoesNotExist:
            return Response({'detail': 'Facility not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
