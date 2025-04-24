from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from facilities.models import Facilities
from facilities.serializers import FacilitySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPageNumberPagination
class FacilityApi(APIView):
    serializer_class = FacilitySerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            ALLOWED_PARAMS = {"status", "is_featured", "created_at", "search", "page_size", "page"}
            unexpected = set(request.query_params.keys()) - ALLOWED_PARAMS
            if unexpected:
                return Response(
                    {"detail": f"Unexpected query parameter(s): {', '.join(unexpected)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                facilities = Facilities.objects.all().order_by("-id")

                # Sort by created_at if passed in query params
                try:
                    created_at = request.query_params.get("created_at", None)
                    if created_at:
                        if created_at == "latest":
                            facilities = facilities.order_by("-created_at")
                        elif created_at == "oldest":
                            facilities = facilities.order_by("created_at")
                        else:
                            facilities = facilities.order_by("-id")
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Filter by status
                try:
                    status_filter = request.query_params.get("status", None)
                    if status_filter is not None:
                        if status_filter.lower() == 'true':
                            facilities = facilities.filter(status=True)
                        elif status_filter.lower() == 'false':
                            facilities = facilities.filter(status=False)
                        else:
                            return Response(
                                {"detail": 'Invalid value for status. Must be "true" or "false".'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Filter by is_featured
                is_featured = request.query_params.get("is_featured", None)
                if is_featured is not None:
                    try:
                        if is_featured.lower() == 'true':
                            facilities = facilities.filter(is_featured=True)
                        elif is_featured.lower() == 'false':
                            facilities = facilities.filter(is_featured=False)
                        else:
                            return Response({
                                'detail': 'Invalid value for is_featured. Must be "true" or "false".'
                            }, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Search by heading
                try:
                    search = request.query_params.get("search", None)
                    if search:
                        facilities = facilities.filter(heading__istartswith=search)
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Pagination
                paginator = CustomPageNumberPagination()
                paginated_queryset = paginator.paginate_queryset(facilities, request)
                serializer = FacilitySerializer(paginated_queryset, many=True, context={'request': request})
                return paginator.get_paginated_response(serializer.data)

            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                facility = Facilities.objects.get(id=pk)
                serializer = FacilitySerializer(facility, context={'request': request})
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
        if 'icon' in request.data:
            if facility.icon:
                facility.icon.delete()
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
        if 'icon' in request.data:
            if facility.icon:
                facility.icon.delete()
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
