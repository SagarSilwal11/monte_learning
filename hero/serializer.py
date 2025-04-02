from rest_framework import serializers
from hero.models import Hero
from django.core.exceptions import ValidationError
from common.models import ImageContent,Image
from django.contrib.contenttypes.models import ContentType



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields=["id","image"]


class ImageContentSerializer(serializers.ModelSerializer):
    image=ImageSerializer()  # Nested serializer to return actual image details
    class Meta:
        model=ImageContent
        fields=['id','image']


class HeroSerializers(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()# Dynamic fetch the data for the hero
    class Meta:
        model=Hero
        fields=['id', 'heading', 'content', 'created_at', 'updated_at', 'is_featured', 'status', 'images']
    

    def get_images(self,obj):
        content_type=ContentType.objects.get_for_model(Hero)
        images=ImageContent.objects.filter(content_type=content_type,object_id=obj.id)
        return [image.image.image.url for image in images]


    def validate_content(self,value):
        if len(value)<=10:
          raise ValidationError("Please provide the content longer the 10 characters")
        if len(value) > 200:
            raise ValidationError("Please provide a content shorter than 200 characters.")
        return value

    def create(self,validated_data):
        # create the a new hero and save images attached to the hero
        request=self.context['request']
        image_data=request.FILES.getlist('images') if request.FILES.getlist('images') else [request.FILES.get('image')]# handle both single and multipe image

        hero=Hero.objects.create(**validated_data)
        content_type=ContentType.objects.get_for_model(Hero)

        for img in image_data:
            image_obj=Image.objects.create(image=img)
            ImageContent.objects.create(content_type=content_type,object_id=hero.id,image_id=image_obj.id)

        return  hero