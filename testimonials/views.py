from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from testimonials.models import Testimonials
from testimonials.serializers import TestimonialSerializer
from common.pagination import CustomPageNumberPagination  # Ensure this exists

class TestimonialsApi(APIView):
    serializer_class = TestimonialSerializer

    def get(self, request, pk=None):
        if pk is None:
            ALLOWED_PARAMS = {"is_active", "created_at", "search", "page_size", "page"}
            unexpected = set(request.query_params.keys()) - ALLOWED_PARAMS
            if unexpected:
                return Response(
                    {"detail": f"Unexpected query parameter(s): {', '.join(unexpected)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                testimonials = Testimonials.objects.all().order_by("-id")

                # Sort by created_at if passed in query params
                created_at = request.query_params.get("created_at", None)
                if created_at:
                    if created_at == "latest":
                        testimonials = testimonials.order_by("-created_at")
                    elif created_at == "oldest":
                        testimonials = testimonials.order_by("created_at")
                    else:
                        testimonials = testimonials.order_by("-id")

                # Filter by is_active
                is_active = request.query_params.get("is_active", None)
                if is_active is not None:
                    if is_active.lower() == 'true':
                        testimonials = testimonials.filter(is_active=True)
                    elif is_active.lower() == 'false':
                        testimonials = testimonials.filter(is_active=False)
                    else:
                        return Response(
                            {"detail": 'Invalid value for is_active. Must be "true" or "false".'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Search by name
                search = request.query_params.get("search", None)
                if search:
                    testimonials = testimonials.filter(name__icontains=search)

                # Pagination
                paginator = CustomPageNumberPagination()
                paginated_queryset = paginator.paginate_queryset(testimonials, request)
                serializer = TestimonialSerializer(paginated_queryset, many=True, context={"request": request})
                return paginator.get_paginated_response(serializer.data)

            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                testimonial = Testimonials.objects.get(id=pk)
                serializer = TestimonialSerializer(testimonial, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Testimonials.DoesNotExist:
                return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = TestimonialSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            testimonial = Testimonials.objects.get(id=pk)
        except Testimonials.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'image' in request.data:
            if testimonial.image:
                testimonial.image.delete()
        serializer = TestimonialSerializer(testimonial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            testimonial = Testimonials.objects.get(id=pk)
        except Testimonials.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'image' in request.data:
            if testimonial.image:
                testimonial.image.delete()
        serializer = TestimonialSerializer(testimonial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            testimonial = Testimonials.objects.get(id=pk)
            testimonial.delete()
            return Response({'detail': 'Testimonial deleted successfully'}, status=status.HTTP_200_OK)
        except Testimonials.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)