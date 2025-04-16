from common.models import Image
from rest_framework import serializers

class ImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields="__all__"