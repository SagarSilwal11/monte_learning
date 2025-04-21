from common.models import Image,ImageContent
from rest_framework import serializers

class ImageSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields="__all__"

class ImageContentSerializer(serializers.ModelSerializer):
    image=ImageSerailizer()
    class Meta:
        model=ImageContent
        fields=[
            "id",'relation_type',
            'image'
        ]

    def create(self,validated_data):
        image_data=validated_data.pop('image')
        image=Image.objects.create(**image_data)
        return ImageContent.objects.create(image=image,**validated_data)