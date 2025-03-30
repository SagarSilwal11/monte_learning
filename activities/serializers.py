from rest_framework import serializers
from activities.models import ActivitiesModel
from django.core.exceptions import ValidationError
from django.conf import settings
class ActivitiesModelSerializers(serializers.ModelSerializer):
    # image=serializers.SerializerMethodField()# custom method for full url
    # def get_image(self,obj):
    #     request=self.context.get("request")# get request context
    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)
    #     else:
    #         return None
    image=serializers.ImageField(use_url=True)
    class Meta:
        model=ActivitiesModel
        fields="__all__"

    def validate_content(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the content longer the 10 characters")
        if len(value) > 200:
            raise ValidationError("Please provide a content shorter than 200 characters.")
        return value