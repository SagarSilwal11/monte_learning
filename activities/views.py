from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from activities.models import ActivitiesModel
from activities.serializers import ActivitiesModelSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ActivityApi(APIView):
    serializer_class = ActivitiesModelSerializers
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                activities = ActivitiesModel.objects.all()
                if not activities:
                    return Response({'detail': 'No activities found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = ActivitiesModelSerializers(activities, many=True,context={"request":request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                activity = ActivitiesModel.objects.get(id=pk)
                serializer = ActivitiesModelSerializers(activity,context={"request":request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ActivitiesModel.DoesNotExist:
                return Response({'detail': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = ActivitiesModelSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            activity = ActivitiesModel.objects.get(id=pk)
        except ActivitiesModel.DoesNotExist:
            return Response({'detail': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ActivitiesModelSerializers(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            activity = ActivitiesModel.objects.get(id=pk)
        except ActivitiesModel.DoesNotExist:
            return Response({'detail': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ActivitiesModelSerializers(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            activity = ActivitiesModel.objects.get(id=pk)
            activity.delete()
            return Response({'detail': 'Activity deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ActivitiesModel.DoesNotExist:
            return Response({'detail': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
