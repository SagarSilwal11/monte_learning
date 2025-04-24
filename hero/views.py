from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hero.models import Hero
from hero.serializer import HeroSerializers
from rest_framework import status
from common.pagination import CustomPageNumberPagination




class HeroApi(APIView):
    serializer_class = HeroSerializers

    
    def get(self, request, pk=None):
        if pk is None:
            ALLOWED_PARAMS = {"status", "is_featured", "created_at", "search","page_size","page"}
            unexpected = set(request.query_params.keys()) - ALLOWED_PARAMS
            if unexpected:
                return Response(
                    {"detail": f"Unexpected query parameter(s): {', '.join(unexpected)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                heroes = Hero.objects.all().order_by("-id")
                # Only sort by 'created_at' if passed in query params
                try:
                    created_at=request.query_params.get("created_at",None)
                    if created_at:
                        if created_at=="latest":
                            heroes=heroes.order_by("-created_at")
                        elif created_at=="oldest":
                            heroes=heroes.order_by("created_at")
                        # elif created_at=="ascending":
                        #     heroes=heroes.order_by("heading")
                        # elif created_at=="descending":
                        #     heroes=heroes.order_by("-heading")
                        else:
                            heroes=heroes.order_by("-id")
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


                try:
                    status_filter=request.query_params.get("status",None)
                    if status_filter is not None:
                            if status_filter.lower()=='true':
                                heroes=heroes.filter(status=True)
                            elif status_filter.lower()=='false':
                                heroes=heroes.filter(status=False)
                            else:
                                return Response ({"detail":'Invalid value for status'},status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                        return Response({'detail':"str(e)"},status=status.HTTP_400_BAD_REQUEST)
                
                featured_filter=request.query_params.get("is_featured",None)
                if featured_filter is not None:
                    try:
                        if featured_filter.lower()=='true':
                            heroes=heroes.filter(is_featured=True)
                        elif featured_filter.lower()=='false':
                            heroes=heroes.filter(is_featured=False)
                        else:
                            return Response({
                                'detail':'Invalid value for the featured'
                            },status=status.HTTP_400_BAD_REQUEST)
                    except:
                        return Response({'detail':"Invalid value"},status=status.HTTP_400_BAD_REQUEST)
            
                try:
                    search = request.query_params.get("search", None)
                    if search:
                            heroes = heroes.filter(heading__istartswith=search)
                except Exception as e:
                    return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # if not heroes:
                #     return Response({'details': 'No heroes found'}, status=status.HTTP_404_NOT_FOUND)
                #applying the paginator
                paginator=CustomPageNumberPagination()
                paginated_queryset=paginator.paginate_queryset(heroes,request)
                serializer = HeroSerializers(paginated_queryset, many=True,context={"request":request})
                return paginator.get_paginated_response(serializer.data)
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
        if 'image' in request.data:
            if hero.image:
                hero.image.delete()
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
        if 'image' in request.data:
            if hero.image:
                hero.image.delete()
        serializer = HeroSerializers(hero, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            hero = Hero.objects.get(id=pk)
            hero.delete()
            return Response({'detail': 'Hero deleted successfully'}, status=status.HTTP_200_OK)
        except Hero.DoesNotExist:
            return Response({'detail': 'Hero not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
