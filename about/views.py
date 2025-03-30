from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from about.serializers import AboutModelSerializers
from about.models import AboutModel
# Create your views here.
class AboutApi(ReadOnlyModelViewSet):
    queryset=AboutModel.objects.all()
    serializer_class=AboutModelSerializers