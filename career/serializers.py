from career.models import CareerModel
from rest_framework import serializers
from django.core.exceptions import ValidationError
class CareerModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=CareerModel
    
    def validate_content(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the content longer the 10 characters")
        if len(value) > 200:
            raise ValidationError("Please provide a content shorter than 200 characters.")
        return value