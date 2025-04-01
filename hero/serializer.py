from rest_framework import serializers
from hero.models import Hero
from django.core.exceptions import ValidationError
from common.models import ImageContent


class HeroSerializers(serializers.ModelSerializer):
    class Meta:
        model=Hero
        fields="__all__"
    
    def validate_content(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the content longer the 10 characters")
        if len(value) > 200:
            raise ValidationError("Please provide a content shorter than 200 characters.")
        return value

class ImageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageContent
        fields=["url"]