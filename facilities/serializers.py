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
    short_content=serializers.SerializerMethodField()
    class Meta:
        model=ActivitiesModel
        fields=['id',
            'image', 'heading', 'content', 'created_at', 'updated_at', 'is_featured', 'status', 'keywords', 'description', 'slug','short_content']

    def get_short_content(self,obj):
        return obj.content[:100] + '...' if len(obj.content)> 100 else obj.content


    def validate_content(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the content longer the 10 characters")
        if len(value) > 200:
            raise ValidationError("Please provide a content shorter than 200 characters.")
        return value