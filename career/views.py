from django.shortcuts import render
from career.models import CareerModel
from career.serializers import CareerModelSerializers
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.

class CareerModelApi(ReadOnlyModelViewSet):
    queryset=CareerModel.objects.all()
    serializer_class=CareerModelSerializers