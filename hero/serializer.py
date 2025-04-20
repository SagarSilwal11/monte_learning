# from rest_framework import serializers
# from hero.models import Hero
# from django.core.exceptions import ValidationError
# class HeroSerializers(serializers.ModelSerializer):
#     image=serializers.ImageField(use_url=True)
#     class Meta:
#         model=Hero
#         fields="__all__"
    
#     def validate_content(self,value):
#         if len(value)<=10:
#           raise ValidationError("Please provide the content longer the 10 characters")
#         if len(value) > 200:
#             raise ValidationError("Please provide a content shorter than 200 characters.")
#         return value
    
from rest_framework import serializers
from hero.models import Hero
from common.models import Image, ImageContent
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

class HeroSerializers(serializers.ModelSerializer):
    image_id = serializers.IntegerField(write_only=True, required=False)
    image_data = serializers.SerializerMethodField()

    class Meta:
        model = Hero
        fields = ['id', 'heading', 'content','created_at',
        'updated_at',
        'is_featured', 'status', 'image_id', 'image_data']


    def get_image_data(self, obj):
        image_link = obj.media_items.filter(relation_type='main_image').first()
        if image_link:
            image = image_link.image
            request = self.context.get('request')  # Get the request object from the serializer context
            absolute_url = request.build_absolute_uri(image.file.url) if request else image.file.url
            return {
                "id": image.id,
                "name": image.name,
                "url": absolute_url,
                "alt_text": image.alt_text,
                "caption": image.caption,
                "source": image.source,
                "mime_type": image.mime_type,
                "size": image.size,
            }
        return None

    def validate_image_id(self,value):
        if value and not Image.objects.filter(id=value).exists():
            raise ValidationError(f"Image with Id {value} doesn't exist")
        return value 
    
    def create(self, validated_data):
        image_id = validated_data.pop('image_id', None)
        hero = Hero.objects.create(**validated_data)
        
        if image_id:
            content_type = ContentType.objects.get_for_model(hero)
            ImageContent.objects.create(
                content_type=content_type,
                object_id=hero.id,
                image_id=image_id,
                relation_type='main_image'
            )
        return hero

    def update(self, instance, validated_data):
        image_id = validated_data.pop('image_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if image_id:
            content_type = ContentType.objects.get_for_model(instance)
            # Remove old and set new
            instance.media_items.filter(relation_type='main_image').delete()
            ImageContent.objects.create(
                content_type=content_type,
                object_id=instance.id,
                image_id=image_id,
                relation_type='main_image' 
            )

        return instance