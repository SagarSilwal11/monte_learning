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

                # Sorting based on 'created_at' if passed in query params
                created_at = request.query_params.get("created_at", None)
                if created_at:
                    if created_at == "latest":
                        activities = activities.order_by("-created_at")
                    elif created_at == "oldest":
                        activities = activities.order_by("created_at")
                    elif created_at == "ascending":
                        activities = activities.order_by("heading")
                    elif created_at == "descending":
                        activities = activities.order_by("-heading")

                # Filtering by 'status' if passed in query params
                status_filter = request.query_params.get("status", None)
                if status_filter is not None:
                    try:
                        if status_filter.lower() == 'true':
                            activities = activities.filter(status=True)
                        elif status_filter.lower() == 'false':
                            activities = activities.filter(status=False)
                        else:
                            return Response({"detail": 'Invalid value for status. Must be "true" or "false".'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except ValueError:
                        return Response({'detail': "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)

                # If no activities found
                if not activities.exists():
                    return Response({'detail': 'No activities found'}, status=status.HTTP_404_NOT_FOUND)

                # Serialize the data and return the response
                serializer = ActivitiesModelSerializers(activities.order_by("-id"), many=True, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                # Fetching specific activity by pk
                activity = ActivitiesModel.objects.get(id=pk)
                serializer = ActivitiesModelSerializers(activity, context={"request": request})
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
