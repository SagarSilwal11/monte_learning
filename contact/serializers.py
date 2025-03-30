from contact.models import ContactModel
from rest_framework import serializers
from django.core.exceptions import ValidationError


class ContactSerializers(serializers.ModelSerializer):
    message=serializers.CharField(required=False,allow_blank=True)
    class Meta:
        
        model=ContactModel
        fields="__all__"
    

    # def validate_name(self,value):

        
    #     if len(value)<2:
    #         raise ValidationError("Name must be more the 2 character")
    #     return value
    
    def validate_message(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the message longer the 10 characters")
        if len(value) > 500:
            raise ValidationError("Please provide a message shorter than 500 characters.")
        return value